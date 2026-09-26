"""Regressions for content the old plain-text extraction misrepresented."""

import pytest

from phission.models import ContentStatus
from phission.parsing import parse_message


def parse_html(body):
    return parse_message(f"Content-Type: text/html; charset=utf-8\n\n{body}".encode(), "html")


@pytest.mark.parametrize(
    "body",
    ['<img src="cid:notice">', "<svg><text>Picture text</text></svg>", "<canvas></canvas>"],
)
def test_visual_only_html_is_not_a_readable_no_links_message(body):
    message = parse_html(body)
    assert message.content_status == ContentStatus.UNSUPPORTED
    assert message.links == ()
    assert message.notes


def test_readable_text_with_uninspected_image_has_partial_coverage():
    message = parse_html('<p>A readable note.</p><img src="https://image.test/pixel">')
    assert message.content_status == ContentStatus.PARTIAL
    assert message.body == "A readable note."
    assert message.links == ()


def test_image_only_anchor_still_exposes_its_inspectable_destination():
    message = parse_html('<a href="https://target.test"><img src="cid:button"></a>')
    assert message.content_status == ContentStatus.PARTIAL
    assert [link.url for link in message.links] == ["https://target.test"]


@pytest.mark.parametrize("tag", ["td", "th", "h3", "h4", "h5", "h6", "section", "pre", "dt", "dd"])
def test_layout_boundaries_cannot_create_a_different_destination(tag):
    message = parse_html(f"<{tag}>https://one.test</{tag}><{tag}>Details</{tag}>")
    assert [link.url for link in message.links] == ["https://one.test"]
    assert "https://one.testDetails" not in message.body


@pytest.mark.parametrize("gap", ['<img src="cid:notice">', "<hr>", "<script>hidden</script>"])
def test_omitted_content_does_not_join_neighboring_text_into_a_url(gap):
    message = parse_html(f"https://one.test{gap}Details")
    assert [link.url for link in message.links] == ["https://one.test"]
