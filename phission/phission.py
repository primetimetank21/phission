# type: ignore
# pylint: disable=no-member, no-value-for-parameter, redefined-outer-name,fixme

# TODOs...
# TODO: connect Gmail API
#   - format specific email page
#   - have IPQS API called only on specific email page user clicks on

# TODO: add types to user output (i.e., phishing=True, malware=False, is_suspicious=True, etc.)
# Dr. Washington TODOs:
#   - add more exaggerated content (i.e., tts for warnings/danger, green/yellow/red for score, flashing for warnings/danger, etc.) => more animations?
#       => emojis: https://thecleverprogrammer.com/2022/06/15/print-emojis-using-python/
#   - add more context (i.e., "About" landing page, "Help me" guide, simple explanation of score and purpose, etc.) => optional?
#   - emotional API: https://humeai.github.io/hume-python-sdk/0.1.6/
#   - implement one of these (for emotional data analysis): https://thecleverprogrammer.com/2021/08/24/sarcasm-detection-with-machine-learning/


# TODO: connect TTS API

import pynecone as pc
from time import sleep
from email_lib import get_all_messages
from phishing_lib import get_IPQS
from .styles import app_style
from components import (
    # button_component,
    # score_display_component,
    # input_component,
    email_panel_component,
)
from components.email_panel import set_email_page_routes


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
        reloads = 3
        emails = []
        while len(emails) == 0:
            if reloads >= 0:
                try:
                    emails = get_all_messages()
                    print(f"Length of email_messages: {len(emails)}")
                    set_email_page_routes(emails, app)
                    self.email_messages = emails
                    break
                except Exception as e:  # pylint: disable=broad-exception-caught
                    print(f"Error in 'get_emails()': {e}")
                finally:
                    reloads -= 1
                    sleep(5)
            else:
                break

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


class EmailPanelState(State):
    text_color: str = "black"
    button_color_scheme: str = "green"

    @pc.var
    def number_of_email_messages(self):
        return len(self.email_messages)

    @pc.var
    def email_message_subjects(self) -> list:
        if len(self.email_messages) == 0:
            return []

        subjects = [email["Subject"] for email in self.email_messages]
        print(f"email_message_subjects:{subjects}")
        return subjects

    @pc.var
    def display_email_message_subjects(self):
        if len(self.email_messages) > 0:
            return True
        else:
            return False


@pc.route(route="/", title="Phissi👁️n Home")
def index() -> pc.Component:
    return pc.center(
        pc.vstack(
            pc.heading("Welcome to Phissi👁️n!", font_size="2em"),
            # score_display_component(State),
            email_panel_component(EmailPanelState),
            # input_component(State),
            # button_component(State),
            spacing="1.5em",
            font_size="1.75em",
        ),
        # vstack formatting
        style=app_style,
    )


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index, route="/", on_load=State.get_emails)
app.compile()
