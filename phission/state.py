"""Per-session Reflex state. Fixed message IDs, explicit actions, no persistence."""

import reflex as rx

from phission.demo import analyze_fixture, load_inbox
from phission.models import ContentStatus, ExtractedLink, Message, ScanOutcome

EMPTY_MESSAGE = Message("", "Choose a message", "", "", "", "", "", (), ContentStatus.UNSUPPORTED)


class DemoState(rx.State):
    messages: list[Message] = []
    inbox_status: str = "loading"
    selected_id: str = ""
    selected_url: str = ""
    analysis_phase: str = "idle"
    outcome: ScanOutcome | None = None
    notice: str = "Loading the synthetic inbox."

    def _clear_analysis(self) -> None:
        self.selected_url = ""
        self.analysis_phase = "idle"
        self.outcome = None

    @rx.event
    def load(self):
        self.inbox_status = "loading"
        self.messages = []
        self.selected_id = ""
        self._clear_analysis()
        self.notice = "Loading the synthetic inbox."
        yield
        try:
            self.messages = load_inbox()
        except OSError:
            self.inbox_status = "error"
            self.notice = "The demo inbox could not load. Try loading the examples again."
            return
        if not self.messages:
            self.inbox_status = "empty"
            self.notice = "No synthetic examples are available."
            return
        self.inbox_status = "ready"
        self.selected_id = self.messages[0].id
        self.notice = "Synthetic inbox ready. Choose a message, then a link to inspect."

    @rx.event
    def select_message(self, message_id: str):
        self._clear_analysis()
        if message_id not in {message.id for message in self.messages}:
            self.selected_id = ""
            self.notice = "That demo message is unavailable. Choose one from the list."
            return
        self.selected_id = message_id
        self.notice = f"Selected: {self.current_message.subject}."

    @rx.event
    def select_link(self, url: str):
        self._clear_analysis()
        if url not in {link.url for link in self.current_message.links}:
            self.notice = "That link is not in the selected message."
            return
        self.selected_url = url
        self.notice = "Link selected. Run demo analysis to reveal its simulated result."

    @rx.event
    def analyze(self):
        message_id, url = self.selected_id, self.selected_url
        self.outcome = None
        if not url or url not in {link.url for link in self.current_message.links}:
            self.analysis_phase = "idle"
            self.notice = "Choose a link in this message first."
            return
        self.analysis_phase = "loading"
        self.notice = "Reading the local demo result. No destination is being visited."
        yield
        outcome = analyze_fixture(message_id, url)
        # Keep target binding even if this implementation later becomes asynchronous.
        if (message_id, url) != (self.selected_id, self.selected_url):
            return
        self.outcome = outcome
        self.analysis_phase = "complete"
        self.notice = f"Simulated result: {outcome.title}."

    @rx.var
    def current_message(self) -> Message:
        return next(
            (message for message in self.messages if message.id == self.selected_id),
            EMPTY_MESSAGE,
        )

    @rx.var
    def links(self) -> list[ExtractedLink]:
        return list(self.current_message.links)

    @rx.var
    def coverage(self) -> str:
        match self.current_message.content_status:
            case ContentStatus.ANALYZED:
                return "Inline text and HTML links inspected. Attachments are never opened."
            case ContentStatus.PARTIAL:
                return "Partial coverage. " + " ".join(self.current_message.notes)
            case ContentStatus.MALFORMED:
                return "Not analyzed: this message could not be read reliably."
            case _:
                return "Not analyzed: this message has no supported inline text."

    @rx.var
    def empty_links_title(self) -> str:
        if self.current_message.content_status in {
            ContentStatus.UNSUPPORTED,
            ContentStatus.MALFORMED,
        }:
            return "Links could not be analyzed"
        return "No HTTP(S) links found in readable text"

    @rx.var
    def result_visible(self) -> bool:
        return bool(
            self.outcome
            and self.outcome.message_id == self.selected_id
            and self.outcome.url == self.selected_url
        )

    @rx.var
    def result_title(self) -> str:
        return self.outcome.title if self.result_visible else ""

    @rx.var
    def result_explanation(self) -> str:
        return self.outcome.explanation if self.result_visible else ""

    @rx.var
    def result_guidance(self) -> str:
        return self.outcome.guidance if self.result_visible else ""

    @rx.var
    def result_score(self) -> str:
        if not self.result_visible or self.outcome.score is None:
            return "No usable score"
        return f"Fixture score: {self.outcome.score} / 100"

    @rx.var
    def result_tone(self) -> str:
        if not self.result_visible or self.outcome.score is None:
            return "unknown"
        if self.outcome.score >= 85:
            return "high"
        if self.outcome.score >= 75:
            return "caution"
        return "low"
