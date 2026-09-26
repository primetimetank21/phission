"""Validate IPQS-shaped fixture responses. There is deliberately no HTTP adapter."""

from phission.models import ScanOutcome, ScanStatus

VERIFY_GUIDANCE = (
    "Pause before sharing information. Open a known app or type a trusted address "
    "yourself; verify unexpected requests through a contact you already know."
)


def normalize_response(payload: object, message_id: str, url: str) -> ScanOutcome:
    """A score is an indicator, not a probability or a safety guarantee.

    Only an explicit boolean success and an integer 0–100 count as a usable result.
    Provider messages are not reflected into the UI (they may contain private data).
    """
    if not isinstance(payload, dict) or type(payload.get("success")) is not bool:
        return ScanOutcome(
            message_id,
            url,
            ScanStatus.ERROR,
            None,
            "Result could not be interpreted",
            "The simulated response has an invalid success field. No score is usable.",
            VERIFY_GUIDANCE,
        )
    if payload["success"] is False:
        return ScanOutcome(
            message_id,
            url,
            ScanStatus.UNKNOWN,
            None,
            "No verdict available",
            "This fixture simulates an unavailable scan. Missing information is not "
            "evidence that a destination is safe.",
            VERIFY_GUIDANCE,
        )
    score = payload.get("risk_score")
    if type(score) is not int or not 0 <= score <= 100:
        return ScanOutcome(
            message_id,
            url,
            ScanStatus.ERROR,
            None,
            "Result could not be interpreted",
            "The simulated response has an invalid score. No score is usable.",
            VERIFY_GUIDANCE,
        )
    if score >= 85:
        title = "High concern"
        explanation = (
            "This fixture represents a strong warning signal. Urgency, credential "
            "requests and an unfamiliar destination deserve independent verification."
        )
    elif score >= 75:
        title = "Reasons for caution"
        explanation = (
            "This fixture represents a suspicious signal. Compare the actual "
            "destination with what the message claims before taking any action."
        )
    else:
        title = "Lower signal, not a guarantee"
        explanation = (
            "This fixture has a lower reputation score. Even a score of zero does "
            "not prove a message or destination is safe. Context still matters."
        )
    return ScanOutcome(
        message_id, url, ScanStatus.SUCCESS, score, title, explanation, VERIFY_GUIDANCE
    )
