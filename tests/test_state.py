from dataclasses import replace

import pytest

from phission import demo
from phission.models import ContentStatus, ScanStatus
from phission.parsing import parse_message
from phission.state import DemoState


@pytest.fixture
def state():
    # Reflex explicitly allows direct state construction in the test environment.
    value = DemoState()
    list(value.load())
    return value


def analyze_first(state):
    state.select_link(state.links[0].url)
    list(state.analyze())


def test_inbox_loading_then_terminal_ready():
    state = DemoState()
    event = state.load()
    next(event)
    assert state.inbox_status == "loading"
    assert not state.messages
    list(event)
    assert state.inbox_status == "ready"
    assert state.selected_id == "library"
    assert len(state.messages) == 5
    assert state.selected_url == ""
    assert not state.result_visible


def test_analysis_requires_explicit_link_selection(state):
    list(state.analyze())
    assert state.analysis_phase == "idle"
    assert not state.result_visible
    assert "Choose a link" in state.notice
    state.select_link(state.links[0].url)
    assert not state.result_visible
    event = state.analyze()
    next(event)
    assert state.analysis_phase == "loading"
    assert not state.result_visible
    list(event)
    assert state.result_visible
    assert state.outcome.status == ScanStatus.SUCCESS
    assert state.result_score == "Fixture score: 0 / 100"
    assert state.result_tone == "low"


def test_message_and_link_switch_clear_previous_result(state):
    analyze_first(state)
    state.select_link(state.links[1].url)
    assert state.outcome is None
    assert not state.result_visible
    list(state.analyze())
    assert state.outcome.score == 12
    state.select_message("urgent")
    assert not state.result_visible
    assert state.outcome is None
    assert state.selected_url == ""
    analyze_first(state)
    assert state.outcome.score == 96
    assert state.outcome.message_id == "urgent"
    assert state.result_tone == "high"


def test_switch_during_analysis_cannot_publish_a_stale_result(state):
    state.select_link(state.links[0].url)
    event = state.analyze()
    next(event)
    state.select_message("urgent")
    list(event)
    assert state.outcome is None
    assert state.analysis_phase == "idle"


def test_outcome_is_hidden_if_target_binding_does_not_match(state):
    analyze_first(state)
    state.outcome = replace(state.outcome, message_id="another-message")
    assert not state.result_visible
    assert not state.result_title
    assert not state.result_explanation


def test_invalid_message_and_url_fail_closed(state):
    analyze_first(state)
    state.select_link("https://arbitrary.test/?secret=demo")
    assert state.selected_url == ""
    assert state.outcome is None
    list(state.analyze())
    assert not state.result_visible
    state.select_message("../../token.json")
    assert state.selected_id == ""
    assert state.current_message.id == ""
    assert state.links == []
    assert "unavailable" in state.notice


def test_sessions_are_independent(state):
    another = DemoState()
    list(another.load())
    state.select_message("urgent")
    analyze_first(state)
    assert another.selected_id == "library"
    assert another.selected_url == ""
    assert another.outcome is None
    assert another.messages is not state.messages


def test_unknown_is_not_success_or_safe(state):
    state.select_message("parcel")
    analyze_first(state)
    assert state.result_visible
    assert state.outcome.status == ScanStatus.UNKNOWN
    assert state.result_score == "No usable score"
    assert state.result_tone == "unknown"
    assert "Partial coverage" in state.coverage


def test_error_response_has_explicit_result(state, monkeypatch):
    monkeypatch.setitem(demo._RESPONSES, ("library", state.links[0].url), {"success": True})
    analyze_first(state)
    assert state.outcome.status == ScanStatus.ERROR
    assert state.result_visible
    assert state.result_title == "Result could not be interpreted"
    assert state.result_score == "No usable score"


def test_no_links_distinct_from_not_analyzed(state):
    state.select_message("garden")
    assert state.links == []
    assert state.empty_links_title == "No HTTP(S) links found in readable text"
    for raw in [b"Content-Type: image/png\n\nsynthetic", b""]:
        state.messages = [parse_message(raw, "unreadable")]
        state.select_message("unreadable")
        assert state.empty_links_title == "Links could not be analyzed"
        assert "Not analyzed" in state.coverage


@pytest.mark.parametrize(("messages", "expected"), [([], "empty"), (None, "error")])
def test_empty_and_error_inbox_terminal_states(state, monkeypatch, messages, expected):
    def load():
        if messages is None:
            raise OSError("Synthetic fixture unavailable")
        return messages

    monkeypatch.setattr("phission.state.load_inbox", load)
    list(state.load())
    assert state.inbox_status == expected
    assert not state.messages
    assert state.selected_id == ""
    assert state.outcome is None


def test_one_malformed_fixture_does_not_lose_the_inbox(tmp_path, monkeypatch):
    (tmp_path / "bad.eml").write_bytes(b"")
    (tmp_path / "good.eml").write_bytes(b"Subject: Fine\n\nReadable")
    monkeypatch.setattr(demo, "FIXTURE_DIR", tmp_path)
    monkeypatch.setattr(demo, "DEMO_IDS", ("bad", "good", "missing"))
    messages = demo.load_inbox()
    assert len(messages) == 3
    assert messages[0].content_status == ContentStatus.MALFORMED
    assert messages[1].subject == "Fine"
    assert messages[1].content_status == ContentStatus.ANALYZED
    assert messages[2].content_status == ContentStatus.MALFORMED


def test_missing_fixture_directory_fails_explicitly(tmp_path, monkeypatch):
    monkeypatch.setattr(demo, "FIXTURE_DIR", tmp_path)
    with pytest.raises(OSError, match="Synthetic fixtures unavailable"):
        demo.load_inbox()
