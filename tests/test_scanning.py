import pytest

from phission.demo import analyze_fixture, load_inbox
from phission.models import ScanStatus
from phission.scanning import normalize_response

TARGET = "https://target.test/path?q=one&next=two#fragment"


@pytest.mark.parametrize(
    ("score", "title"),
    [
        (0, "Lower signal, not a guarantee"),
        (74, "Lower signal, not a guarantee"),
        (75, "Reasons for caution"),
        (84, "Reasons for caution"),
        (85, "High concern"),
        (100, "High concern"),
    ],
)
def test_score_boundaries_and_target_binding(score, title):
    result = normalize_response({"success": True, "risk_score": score}, "message-a", TARGET)
    assert result.status == ScanStatus.SUCCESS
    assert result.score == score
    assert result.title == title
    assert (result.message_id, result.url) == ("message-a", TARGET)
    assert "verify" in result.guidance
    assert "%" not in result.explanation
    assert "safe" not in result.title.lower()


@pytest.mark.parametrize(
    "score", [True, False, -1, 101, "0", "75", 75.0, None, [], {}, float("nan")]
)
def test_invalid_score_has_no_usable_score(score):
    result = normalize_response({"success": True, "risk_score": score}, "a", TARGET)
    assert result.status == ScanStatus.ERROR
    assert result.score is None


@pytest.mark.parametrize(
    "payload",
    [None, [], "invalid json", "{", 0, {}, {"risk_score": 0}, {"success": 1}, {"success": "true"}],
)
def test_malformed_payload_or_success_field(payload):
    result = normalize_response(payload, "a", TARGET)
    assert result.status == ScanStatus.ERROR
    assert result.score is None


def test_missing_score_and_provider_failure_are_different():
    assert normalize_response({"success": True}, "a", TARGET).status == ScanStatus.ERROR
    failure = normalize_response(
        {"success": False, "risk_score": 0, "message": "PRIVATE_PROVIDER_TEXT"}, "a", TARGET
    )
    assert failure.status == ScanStatus.UNKNOWN
    assert failure.score is None
    assert "PRIVATE_PROVIDER_TEXT" not in str(failure)


def test_demo_fixtures_are_deterministic_and_cover_every_extracted_destination():
    outcomes = []
    for message in load_inbox():
        for link in message.links:
            first = analyze_fixture(message.id, link.url)
            assert first == analyze_fixture(message.id, link.url)
            outcomes.append(first)
    assert len(outcomes) == 5
    assert [outcome.score for outcome in outcomes] == [0, 12, 96, 80, None]
    assert outcomes[-1].status == ScanStatus.UNKNOWN


def test_same_link_label_in_another_message_cannot_reuse_a_result():
    url = "https://library.example/workshops/repair-cafe"
    assert analyze_fixture("library", url).status == ScanStatus.SUCCESS
    assert analyze_fixture("urgent", url).status == ScanStatus.UNKNOWN
    assert analyze_fixture("library", "https://unlisted.test").status == ScanStatus.UNKNOWN
