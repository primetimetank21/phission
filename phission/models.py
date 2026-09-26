"""Small, framework-independent values. Nothing here performs I/O."""

from dataclasses import dataclass
from enum import StrEnum


class ContentStatus(StrEnum):
    ANALYZED = "analyzed"
    PARTIAL = "partial"
    UNSUPPORTED = "unsupported"
    MALFORMED = "malformed"


@dataclass(frozen=True)
class ExtractedLink:
    url: str
    labels: tuple[str, ...] = ()


@dataclass(frozen=True)
class Message:
    id: str
    subject: str
    sender_name: str
    sender_address: str
    recipient: str
    date: str
    body: str
    links: tuple[ExtractedLink, ...]
    content_status: ContentStatus
    notes: tuple[str, ...] = ()


class ScanStatus(StrEnum):
    SUCCESS = "success"
    UNKNOWN = "unknown"
    ERROR = "error"


@dataclass(frozen=True)
class ScanOutcome:
    message_id: str
    url: str
    status: ScanStatus
    score: int | None
    title: str
    explanation: str
    guidance: str
