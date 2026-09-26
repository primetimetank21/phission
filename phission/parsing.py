"""Bounded RFC822 parsing, not an email renderer or a complete security scanner.

Inspect inline plain text and HTML HTTP(S) anchors without fetching anything.
Original HTML is never returned. Attachments and other MIME types are not analyzed.
"""

import re
import unicodedata
from email import policy
from email.message import Message as MimeMessage
from email.parser import BytesParser
from email.utils import parseaddr
from html.parser import HTMLParser
from urllib.parse import urlsplit

from phission.models import ContentStatus, ExtractedLink, Message

MAX_MESSAGE_BYTES = 256_000
MAX_PARTS = 100
URL_PATTERN = re.compile(r"https?://[^\s<>\"']+", re.IGNORECASE)
BLOCK_TAGS = {
    "address",
    "article",
    "aside",
    "blockquote",
    "br",
    "dd",
    "div",
    "dl",
    "dt",
    "fieldset",
    "figcaption",
    "figure",
    "footer",
    "form",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "header",
    "hr",
    "li",
    "main",
    "nav",
    "ol",
    "p",
    "pre",
    "section",
    "table",
    "tbody",
    "td",
    "tfoot",
    "th",
    "thead",
    "tr",
    "ul",
}
MEDIA_TAGS = {"img", "picture", "video", "audio", "canvas", "iframe", "object", "svg", "embed"}
HIDDEN_TAGS = {
    "script",
    "style",
    "head",
    "template",
    "iframe",
    "object",
    "svg",
    "canvas",
    "video",
    "audio",
}


def plain_text(value: str) -> str:
    """Remove control/bidi formatting characters; retain ordinary Unicode text."""
    return "".join(
        char
        for char in value.replace("\r\n", "\n").replace("\r", "\n")
        if char in "\n\t" or not unicodedata.category(char).startswith("C")
    ).strip()


def is_http_url(value: str) -> bool:
    """Validate syntax only; preserve the exact destination, query and fragment."""
    if any(c.isspace() or unicodedata.category(c).startswith("C") for c in value):
        return False
    try:
        parsed = urlsplit(value)
        return bool(
            parsed.scheme.lower() in {"http", "https"}
            and parsed.hostname
            and parsed.port != 0
            and not any(c in value for c in '<>"\\')
        )
    except ValueError:
        return False


def text_urls(text: str) -> list[str]:
    urls = []
    for match in URL_PATTERN.finditer(text):
        url = match.group().rstrip(".,;:!?")
        for opening, closing in [("(", ")"), ("[", "]"), ("{", "}")]:
            while url.endswith(closing) and url.count(closing) > url.count(opening):
                url = url[:-1]
        if is_http_url(url):
            urls.append(url)
    return urls


class _HTMLText(HTMLParser):
    """Keep visible text and anchor destinations, never markup or embedded media."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.text: list[str] = []
        self.links: list[tuple[str, str]] = []
        self.hidden: list[str] = []
        self.anchor: str | None = None
        self.label: list[str] = []
        self.omitted_media = False

    def _separator(self) -> None:
        self.text.append("\n")
        if self.anchor:
            self.label.append(" ")

    def _finish_anchor(self) -> None:
        if self.anchor:
            self.links.append((self.anchor, plain_text("".join(self.label))))
        self.anchor = None
        self.label = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in MEDIA_TAGS:
            self.omitted_media = True
        if tag in HIDDEN_TAGS:
            self._separator()
            self.hidden.append(tag)
        if self.hidden:
            return
        if tag in BLOCK_TAGS or tag in MEDIA_TAGS:
            self._separator()
        if tag == "a":
            self._finish_anchor()
            href = dict(attrs).get("href") or ""
            self.anchor = href if is_http_url(href) else None

    def handle_endtag(self, tag: str) -> None:
        if self.hidden:
            if tag == self.hidden[-1]:
                self.hidden.pop()
                self._separator()
            return
        if tag == "a":
            self._finish_anchor()
        if tag in BLOCK_TAGS or tag in MEDIA_TAGS:
            self._separator()

    def handle_data(self, data: str) -> None:
        if not self.hidden:
            self.text.append(data)
            if self.anchor:
                self.label.append(data)

    def finish(self) -> tuple[str, list[tuple[str, str]]]:
        self.close()
        self._finish_anchor()
        raw_text = "".join(self.text)
        # Sanitize display text separately: removing a control character must not
        # manufacture a different, apparently valid destination for analysis.
        return plain_text(raw_text), self.links + [(url, "") for url in text_urls(raw_text)]


def parse_message(raw: bytes, message_id: str) -> Message:
    """Return an explicit coverage state even for malformed/unsupported messages.

    Missing headers are harmless. MIME/decoding defects mark partial coverage;
    one bad message must not prevent the rest of a synthetic inbox from loading.
    """
    fallback = Message(
        id=message_id,
        subject="Unreadable message",
        sender_name="Unknown sender",
        sender_address="Not provided",
        recipient="Not provided",
        date="Not provided",
        body="This message could not be analyzed.",
        links=(),
        content_status=ContentStatus.MALFORMED,
        notes=("Malformed message or demo parsing limit exceeded.",),
    )
    if not isinstance(raw, bytes) or not raw or len(raw) > MAX_MESSAGE_BYTES:
        return fallback
    try:
        root = BytesParser(policy=policy.default).parsebytes(raw)
        notes: list[str] = []
        destinations: dict[str, list[str]] = {}
        analyzed = 0
        parts_seen = 0

        def inspect(part: MimeMessage) -> str:
            nonlocal analyzed, parts_seen
            parts_seen += 1
            if parts_seen > MAX_PARTS:
                raise ValueError("Too many MIME parts")
            if part.defects:
                notes.append("Malformed MIME structure; coverage may be incomplete.")
            kind = part.get_content_type()
            if part.get_content_disposition() == "attachment":
                notes.append("Attachments are not analyzed.")
                return ""
            if part.is_multipart() and kind.startswith("multipart/"):
                children = list(part.iter_parts())
                bodies = [inspect(child) for child in children]
                if kind == "multipart/alternative":
                    # Analyze all alternatives, but avoid displaying duplicate bodies.
                    for child, body in zip(children, bodies, strict=True):
                        if child.get_content_type() == "text/plain" and body:
                            return body
                    return next((body for body in bodies if body), "")
                return "\n\n".join(body for body in bodies if body)
            if kind not in {"text/plain", "text/html"}:
                notes.append("Unsupported MIME content is not analyzed.")
                return ""
            payload = part.get_payload(decode=True)
            if not isinstance(payload, bytes):
                notes.append("A text part could not be decoded.")
                return ""
            try:
                text = payload.decode(part.get_content_charset() or "utf-8")
            except (UnicodeError, LookupError):
                notes.append("Some characters could not be decoded reliably.")
                text = payload.decode("utf-8", errors="replace")
            if part.defects:
                notes.append("Malformed transfer encoding; coverage may be incomplete.")
            if kind == "text/html":
                html = _HTMLText()
                html.feed(text)
                body, links = html.finish()
                if html.omitted_media:
                    notes.append("Images and embedded media are not analyzed.")
                if body or links:
                    analyzed += 1
                else:
                    notes.append("HTML has no readable inline text or supported links.")
            else:
                analyzed += 1
                body = plain_text(text)
                links = [(url, "") for url in text_urls(text)]
            for url, label in links:
                labels = destinations.setdefault(url, [])
                if label and label not in labels:
                    labels.append(label)
            return body

        body = inspect(root)
        sender_name, sender_address = parseaddr(str(root.get("From", "")))
        status = ContentStatus.ANALYZED
        if not analyzed:
            status = ContentStatus.UNSUPPORTED
        elif notes:
            status = ContentStatus.PARTIAL
        return Message(
            id=message_id,
            subject=plain_text(str(root.get("Subject", ""))) or "(No subject)",
            sender_name=plain_text(sender_name or sender_address) or "Unknown sender",
            sender_address=plain_text(sender_address) or "Not provided",
            recipient=plain_text(str(root.get("To", ""))) or "Not provided",
            date=plain_text(str(root.get("Date", ""))) or "Not provided",
            body=body or "No readable inline text is available.",
            links=tuple(ExtractedLink(url, tuple(labels)) for url, labels in destinations.items()),
            content_status=status,
            notes=tuple(dict.fromkeys(notes)),
        )
    except (ValueError, TypeError, UnicodeError, LookupError, RecursionError):
        return fallback
