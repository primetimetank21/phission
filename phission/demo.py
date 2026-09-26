"""The only data source: authored local fixtures, with no live-mode switch."""

from pathlib import Path

from phission.models import Message, ScanOutcome
from phission.parsing import parse_message
from phission.scanning import normalize_response

FIXTURE_DIR = Path(__file__).parent / "fixtures"
DEMO_IDS = ("library", "urgent", "benefits", "parcel", "garden")
SCENARIOS = {
    "library": "An everyday notice",
    "urgent": "An urgent request",
    "benefits": "A misleading label",
    "parcel": "An unavailable result",
    "garden": "A note without links",
}
# Keyed by both message and exact destination. Never use a generic Link_N verdict.
_RESPONSES: dict[tuple[str, str], dict[str, object]] = {
    ("library", "https://library.example/workshops/repair-cafe"): {
        "success": True,
        "risk_score": 0,
    },
    ("library", "https://library.example/workshops"): {
        "success": True,
        "risk_score": 12,
    },
    (
        "urgent",
        "https://account-review.test/verify?source=email&step=confirm#account",
    ): {"success": True, "risk_score": 96},
    ("benefits", "https://staff-benefits.test/review?team=people&from=mail"): {
        "success": True,
        "risk_score": 80,
    },
    ("parcel", "https://parcel.example/track/DEMO-204"): {"success": False},
}


def load_inbox() -> list[Message]:
    """Read only the fixed synthetic manifest, never caller-supplied paths."""
    messages = []
    read_count = 0
    for message_id in DEMO_IDS:
        try:
            raw = (FIXTURE_DIR / f"{message_id}.eml").read_bytes()
            read_count += 1
        except OSError:
            raw = b""
        messages.append(parse_message(raw, message_id))
    if not read_count:
        raise OSError("Synthetic fixtures unavailable")
    return messages


def analyze_fixture(message_id: str, url: str) -> ScanOutcome:
    """No URL is visited or sent to a provider, even for an unknown target."""
    return normalize_response(
        _RESPONSES.get((message_id, url), {"success": False}), message_id, url
    )
