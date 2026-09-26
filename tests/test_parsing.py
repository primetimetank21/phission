from email.message import EmailMessage

import pytest

from phission.models import ContentStatus
from phission.parsing import MAX_MESSAGE_BYTES, is_http_url, parse_message


def plain(body: str, **headers: str) -> bytes:
    message = EmailMessage()
    for key, value in headers.items():
        message[key] = value
    message.set_content(body)
    return message.as_bytes()


def urls(message):
    return [link.url for link in message.links]


def test_single_part_unicode_case_varied_headers_and_bare_sender():
    message = parse_message(
        plain(
            "Hello Zoë — café details: https://café.example/été?q=one&b=two#details",
            **{"fRoM": "robin@garden.example", "sUbJeCt": "Café with Zoë"},
        ),
        "unicode",
    )
    assert message.subject == "Café with Zoë"
    assert message.sender_name == message.sender_address == "robin@garden.example"
    assert message.recipient == message.date == "Not provided"
    assert message.content_status == ContentStatus.ANALYZED
    assert urls(message) == ["https://café.example/été?q=one&b=two#details"]
    assert "Zoë — café" in message.body


def test_missing_headers_no_links_is_not_unsupported():
    message = parse_message(plain("Hello there"), "no-headers")
    assert message.subject == "(No subject)"
    assert message.sender_name == "Unknown sender"
    assert message.sender_address == "Not provided"
    assert message.content_status == ContentStatus.ANALYZED
    assert message.links == ()


def test_duplicate_prefix_overlapping_urls_do_not_mutate_body():
    body = (
        "https://library.example/events https://library.example/events/repair "
        "https://library.example/events. (https://library.example/a_(b))."
    )
    message = parse_message(plain(body), "prefixes")
    assert message.body == body
    assert urls(message) == [
        "https://library.example/events",
        "https://library.example/events/repair",
        "https://library.example/a_(b)",
    ]


def test_html_extracts_destination_and_label_without_markup_or_embeds():
    raw = b"""MIME-Version: 1.0
Content-Type: text/html; charset=utf-8

<html><head><title>hidden</title><style>hidden https://style.test</style></head>
<body><p>Hello &amp; welcome</p><script>https://script.test</script>
<a href="https://destination.test/path?x=1&amp;y=2#here">Open <b>staff portal</b></a>
<a href="javascript:alert(1)">Not a web link</a>
<img src="https://image.test/pixel" onerror="alert(1)">
<a href="https://destination.test/path?x=1&amp;y=2#here">Second label</a>
<!-- https://comment.test --></body></html>"""
    message = parse_message(raw, "html")
    assert urls(message) == ["https://destination.test/path?x=1&y=2#here"]
    assert message.links[0].labels == ("Open staff portal", "Second label")
    assert "Hello & welcome" in message.body
    assert "<" not in message.body
    assert "hidden" not in message.body
    assert "https://image.test" not in message.body
    assert "alert(1)" not in message.body


def test_nested_multipart_analyzes_html_even_with_plain_alternative():
    message = EmailMessage()
    message.set_content("Plain alternative: https://plain.example/a")
    message.add_alternative(
        '<p>Alternative</p><a href="https://hidden.test/b">Friendly label</a>',
        subtype="html",
    )
    message.add_attachment(b"https://attachment.test", maintype="application", subtype="pdf")
    parsed = parse_message(message.as_bytes(), "nested")
    assert urls(parsed) == ["https://plain.example/a", "https://hidden.test/b"]
    assert parsed.body == "Plain alternative: https://plain.example/a"
    assert parsed.content_status == ContentStatus.PARTIAL
    assert "Attachments are not analyzed." in parsed.notes


def test_multipart_mixed_preserves_both_text_bodies():
    message = EmailMessage()
    message.make_mixed()
    first = EmailMessage()
    first.set_content("First part")
    second = EmailMessage()
    second.set_content('<a href="https://second.test">Second part</a>', subtype="html")
    message.attach(first)
    message.attach(second)
    parsed = parse_message(message.as_bytes(), "mixed")
    assert parsed.body == "First part\n\nSecond part"
    assert urls(parsed) == ["https://second.test"]


@pytest.mark.parametrize(
    "mime", ["application/pdf", "image/png", "text/calendar", "message/rfc822"]
)
def test_unsupported_is_not_no_links(mime):
    parsed = parse_message(
        f"Content-Type: {mime}\n\nhttps://not-inspected.test".encode(), "unsupported"
    )
    assert parsed.content_status == ContentStatus.UNSUPPORTED
    assert parsed.links == ()
    assert parsed.notes


@pytest.mark.parametrize("raw", [b"", None, b"x" * (MAX_MESSAGE_BYTES + 1)])
def test_bad_input_returns_terminal_malformed_result(raw):
    parsed = parse_message(raw, "broken")
    assert parsed.id == "broken"
    assert parsed.content_status == ContentStatus.MALFORMED
    assert parsed.links == ()


def test_too_many_parts_is_bounded():
    message = EmailMessage()
    message.make_mixed()
    for _ in range(101):
        part = EmailMessage()
        part.set_content("Synthetic content")
        message.attach(part)
    assert parse_message(message.as_bytes(), "many").content_status == ContentStatus.MALFORMED


@pytest.mark.parametrize(
    "raw",
    [
        b"Content-Type: text/plain; charset=unknown-charset\n\nhello \xff https://a.test",
        b"Content-Type: text/plain; charset=utf-8\n\nhello \xff https://a.test",
        b"Content-Type: multipart/mixed; boundary=missing\n\nhello https://a.test",
        b"Content-Transfer-Encoding: base64\n\naGVsbG8=%%%",
        b"Not a header\nhttps://a.test",
    ],
)
def test_malformed_encoding_or_structure_never_claims_full_coverage(raw):
    parsed = parse_message(raw, "malformed")
    assert parsed.content_status != ContentStatus.ANALYZED
    assert parsed.notes


def test_legacy_charset_decoded_without_guessing_utf8():
    parsed = parse_message(
        b"Content-Type: text/plain; charset=iso-8859-1\n\nCaf\xe9 https://cafe.test", "latin"
    )
    assert parsed.body == "Café https://cafe.test"
    assert parsed.content_status == ContentStatus.ANALYZED


def test_unclosed_html_anchor_is_still_extracted():
    parsed = parse_message(
        b'Content-Type: text/html\n\n<p>Hello <a href="https://open.test">unfinished', "html"
    )
    assert urls(parsed) == ["https://open.test"]
    assert parsed.links[0].labels == ("unfinished",)


@pytest.mark.parametrize("mime", [b"text/plain", b"text/html"])
def test_control_characters_removed_from_display_but_not_rewritten_as_destinations(mime):
    raw = plain("Hello\u202e friend https://bad.test/\u202eother", Subject="A\u202eB")
    parsed = parse_message(raw.replace(b"text/plain", mime), "controls")
    assert "\u202e" not in parsed.body
    assert parsed.subject == "AB"
    assert parsed.links == ()


@pytest.mark.parametrize(
    "url",
    [
        "javascript:alert(1)",
        "ftp://files.example",
        "/relative",
        "https://",
        "https://bad.test:wrong",
        "https://bad.test:99999",
        "https://bad.test:0",
        "https://[invalid",
        "https://white space.test",
        "https://a.test/\nother",
        "https://a.test/\u202eb",
        'https://a.test/"quoted',
        "https://a.test\\other",
    ],
)
def test_invalid_urls_rejected(url):
    assert not is_http_url(url)


@pytest.mark.parametrize(
    "url",
    ["http://a.test", "HTTPS://a.test/a?x=1&b=2#frag", "https://a.test:443/", "https://é.test"],
)
def test_http_syntax_does_not_drop_scheme_query_or_fragment(url):
    assert is_http_url(url)
