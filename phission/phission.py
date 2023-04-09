# type: ignore
# pylint: disable=no-member, no-value-for-parameter, redefined-outer-name,fixme

# TODOs...
# TODO: connect Gmail API
# TODO: connect TTS API

import pynecone as pc
from time import sleep
from email_lib import get_all_messages
from phishing_lib import get_IPQS
from .styles import app_style
from components import button_component, score_display_component, input_component


# State
class State(pc.State):
    """The app state."""

    # credentials for Gmail API
    user_email: str = "jhnwck2023@gmail.com"
    user_password: str = "password123EZ"

    # Gmail API messages
    email_messages: list = []

    # index variables
    url: str = ""
    url_display: str = ""
    risk_score: int = None

    # TODO: extract more values from this in set_IPQS
    # TODO: add types to user output (i.e., phishing=True, malware=False, is_suspicious=True, etc.)
    # Dr. Washington TODOs:
    #   [] add more exaggerated content (i.e., tts for warnings/danger, green/yellow/red for score, flashing for warnings/danger, etc.)
    #   [] add more context (i.e., "About" landing page, "Help me" guide, simple explanation of score and purpose, etc.)
    ipqs: dict = {}

    def get_emails(self):
        emails = get_all_messages()
        self.email_messages = emails
        sleep(0.25)
        print(f"Length of email_messages: {len(emails)}")

    @pc.var
    def number_of_email_messages(self):
        return len(self.email_messages)

    @pc.var
    def email_message_subjects(self) -> list:
        if len(self.email_messages) == 0:
            return []

        subjects: list = [email["Subject"] for email in self.email_messages]
        print(f"email_message_subjects:{subjects}")
        return subjects

    @pc.var
    def display_email_message_subjects(self):
        if len(self.email_messages) > 0:
            return True
        else:
            return False

    @pc.var
    def display_score(self):
        if len(self.url_display) > 0 and self.risk_score is not None:
            return True
        else:
            return False

    @pc.var
    def get_risk_str(self) -> str:
        risk_score = self.risk_score
        if risk_score == 0 or not risk_score:
            return "somewhat safe"

        risk_lvl = ""
        if risk_score >= 85:
            risk_lvl = "high risk"
        elif risk_score >= 75:
            risk_lvl = "suspicious"
        else:
            risk_lvl = "somewhat safe"

        return risk_lvl

    def set_IPQS(self):
        url = self.url

        # TODO:
        # make async (?)
        score = get_IPQS(url)
        self.ipqs = score

        # TODO: remove this print statement
        print(score)
        if score:
            self.url_display = url
            self.risk_score = score["risk_score"]


def email_ui(email_data: dict) -> pc.Component:
    return pc.vstack(
        pc.text(email_data["From"]),
        pc.text(email_data["To"]),
        pc.text(email_data["Date"]),
        pc.text(email_data["Subject"]),
        pc.text(email_data["Plain_Text"]),
        pc.text(email_data["URLs"]),
        display="flex",
        align_items="center",
        justify_content="center",
    )


def get_email(subject_index: int, email_dict: dict):
    def email_page() -> pc.Component:
        return email_ui(email_dict)

    @pc.route(route=f"/emails/{subject_index}")
    def email_page_route() -> pc.Component:
        return email_page()

    return email_page_route


class EmailPanelState(State):
    text_color: list = "black"
    button_bg_color: list = "green"

    def get_email_by_subject_index(self, index):
        email = self.email_messages[index]
        get_email(index, email)
        app.compile()
        return pc.redirect(f"http://localhost:3000/emails/{index}")


def email_panel_component(msg: str, index: int):
    return pc.button(
        pc.text(msg, font_size="2em", color="white"),
        is_full_width=True,
        height="75px",
        variant="solid",
        color_scheme="green",
        # on_click goes here...
        on_click=lambda: EmailPanelState.get_email_by_subject_index(index),
    )


@pc.route(route="/", title="Phissi👁️n Home")
def index() -> pc.Component:
    return pc.center(
        pc.vstack(
            pc.heading("Welcome to Phissi👁️n!", font_size="2em"),
            score_display_component(State),
            pc.vstack(
                pc.cond(
                    State.display_email_message_subjects,
                    pc.foreach(
                        State.email_message_subjects,
                        lambda msg, index: email_panel_component(  # pylint: disable=unnecessary-lambda
                            msg, index
                        ),
                    ),
                    pc.text("No messages"),
                )
            ),
            input_component(State),
            button_component(State),
            spacing="1.5em",
            font_size="2em",
        ),
        # vstack formatting
        style=app_style,
    )


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index, on_load=State.get_emails)
app.compile()
