"""One fixed, data-driven Reflex page. Email HTML and URLs are never rendered as links."""

import reflex as rx

from phission.demo import SCENARIOS
from phission.models import ExtractedLink, Message
from phission.state import DemoState as State

HISTORY_URL = (
    "https://github.com/primetimetank21/phission/tree/0ced1f54baccc2ed6abd307d43971e82315c3961"
)


def eyebrow(text: str) -> rx.Component:
    return rx.el.p(text, class_name="eyebrow")


def message_card(message: rx.Var[Message]) -> rx.Component:
    return rx.el.li(
        rx.el.button(
            rx.el.span(
                rx.el.span(message.sender_name, class_name="sender-name"),
                rx.cond(
                    State.selected_id == message.id,
                    rx.el.span("Selected", class_name="selected-tag"),
                ),
                class_name="message-card-top",
            ),
            rx.el.span(message.subject, class_name="message-subject"),
            rx.el.span(
                rx.match(message.id, *SCENARIOS.items(), "Synthetic example"),
                class_name="message-scenario",
            ),
            type="button",
            class_name="message-card",
            on_click=[State.select_message(message.id), rx.set_focus("message-heading")],
            custom_attrs={"aria-pressed": State.selected_id == message.id},
        )
    )


def inbox() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                eyebrow("01 / CHOOSE A MESSAGE"),
                rx.el.h2("The demo inbox", id="inbox-title", tab_index=-1),
            ),
            rx.el.span("5 examples", class_name="count-tag"),
            class_name="panel-heading inbox-heading",
        ),
        rx.el.p("A few familiar situations. A little room to pause.", class_name="muted"),
        rx.el.ul(rx.foreach(State.messages, message_card), class_name="message-list"),
        rx.el.div(
            rx.el.strong("Nothing here is your email."),
            rx.el.p("These messages were written for this demo. Your inbox is never connected."),
            class_name="inbox-note",
        ),
        class_name="inbox",
        custom_attrs={"aria-labelledby": "inbox-title"},
    )


def link_choice(link: rx.Var[ExtractedLink], index: rx.Var[int]) -> rx.Component:
    return rx.el.li(
        rx.el.button(
            rx.el.span(
                rx.el.span("Link ", index + 1, class_name="link-number"),
                rx.cond(
                    State.selected_url == link.url,
                    rx.el.span("Selected", class_name="selected-tag"),
                    rx.el.span("Select to inspect", class_name="link-action"),
                ),
                class_name="link-top",
            ),
            rx.el.span(link.url, class_name="url-text"),
            rx.foreach(
                link.labels,
                lambda label: rx.el.span("Label in email: “", label, "”", class_name="link-label"),
            ),
            type="button",
            class_name="link-choice",
            on_click=State.select_link(link.url),
            custom_attrs={"aria-pressed": State.selected_url == link.url},
        ),
    )


def result() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.span("SIMULATED RESULT", class_name="eyebrow"),
            rx.el.span(State.result_score, class_name="score-label"),
            class_name="result-top",
        ),
        rx.el.h4(
            rx.match(
                State.result_tone,
                ("high", rx.icon("triangle-alert", size=22, aria_hidden=True)),
                ("caution", rx.icon("circle-alert", size=22, aria_hidden=True)),
                ("unknown", rx.icon("circle-help", size=22, aria_hidden=True)),
                rx.icon("info", size=22, aria_hidden=True),
            ),
            State.result_title,
            id="result-title",
        ),
        rx.el.p("For this destination only", class_name="result-target-label"),
        rx.el.p(State.selected_url, class_name="url-text result-target"),
        rx.el.p(State.result_explanation),
        rx.el.div(
            rx.el.strong("A sensible next step"),
            rx.el.p(State.result_guidance),
            class_name="guidance",
        ),
        rx.el.p(
            "A fixture score is not a probability, a live assessment or a safety guarantee.",
            class_name="result-disclaimer",
        ),
        class_name="result",
        custom_attrs={
            "data-tone": State.result_tone,
            "aria-labelledby": "result-title",
        },
    )


def inspector() -> rx.Component:
    return rx.el.section(
        eyebrow("03 / LOOK AT THE DESTINATION"),
        rx.el.h3("A closer look at the links", id="links-heading"),
        rx.el.p(
            "Select a destination, then reveal its demo result. These controls never "
            "open the URL or submit it to a service.",
            class_name="muted",
        ),
        rx.el.p(State.coverage, class_name="coverage"),
        rx.cond(
            State.links.length() > 0,
            rx.el.div(
                rx.el.ul(rx.foreach(State.links, link_choice), class_name="link-list"),
                rx.el.div(
                    rx.el.button(
                        rx.cond(
                            State.analysis_phase == "loading",
                            "Reading local fixture…",
                            "Run demo analysis",
                        ),
                        type="button",
                        on_click=State.analyze,
                        disabled=(State.selected_url == "") | (State.analysis_phase == "loading"),
                        class_name="primary-button",
                    ),
                    rx.el.p(
                        rx.cond(
                            State.selected_url == "",
                            "Choose a link above to begin.",
                            "Deterministic fixture · no live scan",
                        ),
                        class_name="action-hint",
                    ),
                    class_name="analysis-action",
                ),
                rx.cond(State.result_visible, result()),
                custom_attrs={"aria-busy": State.analysis_phase == "loading"},
            ),
            rx.el.div(
                rx.el.strong(State.empty_links_title),
                rx.el.p(
                    "This is not a safety verdict. Requests in the wording, unsupported "
                    "content and attachments can still require caution."
                ),
                class_name="empty-links",
            ),
        ),
        class_name="inspector",
        custom_attrs={"aria-labelledby": "links-heading"},
    )


def reading_pane() -> rx.Component:
    return rx.el.article(
        rx.el.a(
            "← Back to messages",
            href="#inbox-title",
            on_click=rx.set_focus("inbox-title"),
            class_name="back-link",
        ),
        eyebrow("02 / READ WITH A LITTLE DISTANCE"),
        rx.el.h2(State.current_message.subject, id="message-heading", tab_index=-1),
        rx.cond(
            State.selected_id != "",
            rx.el.div(
                rx.el.dl(
                    rx.el.div(
                        rx.el.dt("From"),
                        rx.el.dd(
                            State.current_message.sender_name,
                            rx.el.span(
                                State.current_message.sender_address,
                                class_name="sender-address",
                            ),
                        ),
                    ),
                    rx.el.div(rx.el.dt("To"), rx.el.dd(State.current_message.recipient)),
                    class_name="message-meta",
                ),
                rx.el.div(
                    rx.el.span("SYNTHETIC EMAIL", class_name="email-caption"),
                    rx.el.p(State.current_message.body, class_name="email-body"),
                    class_name="email-paper",
                ),
                rx.el.p(
                    "Plain-text reading view. Original HTML, images and attachments "
                    "are not displayed.",
                    class_name="reading-note",
                ),
                inspector(),
            ),
            rx.el.p("Choose one of the synthetic messages in the demo inbox."),
        ),
        class_name="reading-pane",
        custom_attrs={"aria-labelledby": "message-heading"},
    )


def unavailable_inbox() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            rx.match(
                State.inbox_status,
                ("loading", "Preparing the demo inbox…"),
                ("empty", "No examples available"),
                "The demo inbox could not load",
            )
        ),
        rx.el.p("Only local synthetic fixtures are used. No inbox connection is needed."),
        rx.cond(
            State.inbox_status != "loading",
            rx.el.button(
                "Load examples again",
                type="button",
                on_click=State.load,
                class_name="primary-button",
            ),
        ),
        class_name="unavailable-inbox",
    )


def about() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            eyebrow("A MOMENT OF CLARITY"),
            rx.el.h2("A tool for pausing. Not a promise of safety.", id="about-title"),
            rx.el.p(
                "A familiar name or a reassuring score can miss the bigger picture. "
                "Use this workspace to practice checking the destination and the request.",
                class_name="about-intro",
            ),
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span("01", class_name="step-number"),
                rx.el.h3("Read the request"),
                rx.el.p("Notice pressure, unexpected payments or requests for secrets."),
            ),
            rx.el.div(
                rx.el.span("02", class_name="step-number"),
                rx.el.h3("Check the destination"),
                rx.el.p("A friendly label can hide an unfamiliar address. Compare both."),
            ),
            rx.el.div(
                rx.el.span("03", class_name="step-number"),
                rx.el.h3("Verify another way"),
                rx.el.p("Use a known app or contact, rather than trusting an email link."),
            ),
            class_name="how-grid",
        ),
        rx.el.details(
            rx.el.summary("What this demo does — and does not do"),
            rx.el.p(
                "The MIME parsing, link extraction and response validation are real "
                "code. The emails and reputation responses are authored fixtures. "
                "No mailbox access, live detection, uploads, analytics or external "
                "scanning is available. Not all email formats or threats are covered."
            ),
            rx.el.p(
                "Keyboard controls and readable text are independent of speech. "
                "Read-aloud is not included in this release; use your browser or "
                "assistive technology if available. JavaScript and a running Reflex "
                "server are required for interaction."
            ),
        ),
        id="how-it-works",
        class_name="about",
        custom_attrs={"aria-labelledby": "about-title"},
    )


def index() -> rx.Component:
    return rx.el.div(
        rx.el.a(
            "Skip to demo", href="#demo", on_click=rx.set_focus("demo"), class_name="skip-link"
        ),
        rx.el.header(
            rx.el.a(
                rx.el.img(src="/eye.svg", alt="", width="32", height="32"),
                rx.el.span("Phission"),
                href="/",
                class_name="wordmark",
                custom_attrs={"aria-label": "Phission home"},
            ),
            rx.el.a("How it works ↗", href="#how-it-works", class_name="header-link"),
            class_name="site-header",
        ),
        rx.el.main(
            rx.el.section(
                eyebrow("A CLEARER LOOK AT EMAIL"),
                rx.el.h1("A little pause. ", rx.el.span("A clearer perspective.")),
                rx.el.p(
                    "An unexpected message doesn’t have to rush you. Practice reading "
                    "the signs and looking closer at links — one email at a time.",
                    class_name="hero-description",
                ),
                class_name="hero",
            ),
            rx.el.div(
                rx.el.span("Interactive demo", class_name="demo-badge"),
                rx.el.p(
                    rx.el.strong("Synthetic emails. No inbox connection."),
                    " Every analysis result is simulated, not live detection.",
                ),
                class_name="demo-notice",
            ),
            rx.el.section(
                rx.el.p(
                    State.notice,
                    role="status",
                    class_name="workspace-status",
                    custom_attrs={"aria-live": "polite", "aria-atomic": "true"},
                ),
                rx.cond(
                    State.inbox_status == "ready",
                    rx.el.div(inbox(), reading_pane(), class_name="workspace-grid"),
                    unavailable_inbox(),
                ),
                id="demo",
                tab_index=-1,
                class_name="workspace",
                custom_attrs={"aria-label": "Interactive synthetic email demo"},
            ),
            about(),
            rx.el.noscript(
                "This demo needs JavaScript and a running Reflex server. No mailbox "
                "or scanning service is connected.",
            ),
            class_name="page-main",
        ),
        rx.el.footer(
            rx.el.div(
                rx.el.strong("Phission"),
                rx.el.p("A learning workspace, not a security product."),
            ),
            rx.el.p(
                "Originally built in 2023 for HCI and affective-computing coursework, "
                "with usability testing. The original findings are no longer available. ",
                rx.el.a("View the historical prototype", href=HISTORY_URL),
                ".",
                class_name="history-note",
            ),
            class_name="site-footer",
        ),
    )


app = rx.App(
    stylesheets=["/styles.css"],
    html_lang="en",
    head_components=[rx.el.link(rel="icon", href="/eye.svg", type="image/svg+xml")],
)
app.add_page(
    index,
    route="/",
    title="Phission — a clearer look at email",
    description="A synthetic-only workspace for practicing thoughtful email decisions.",
    on_load=State.load,
    meta=[{"name": "theme-color", "content": "#f7f8f4"}],
)
