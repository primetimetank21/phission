# type: ignore
# pylint: disable=no-member, no-value-for-parameter, redefined-outer-name,fixme

# TODO: add types to user output (i.e., phishing=True, malware=False, is_suspicious=True, etc.)
# Dr. Washington TODOs:
#   - add more exaggerated content (i.e., tts for warnings/danger, green/yellow/red for score, flashing for warnings/danger, etc.) => more animations?
#       => emojis: https://thecleverprogrammer.com/2022/06/15/print-emojis-using-python/
#   - add more context (i.e., "About" landing page, "Help me" guide, simple explanation of score and purpose, etc.) => optional?
#   - emotional API: https://humeai.github.io/hume-python-sdk/0.1.6/
#   - implement one of these (for emotional data analysis): https://thecleverprogrammer.com/2021/08/24/sarcasm-detection-with-machine-learning/


# TODO: connect TTS API
# TODO: style app more!
#   - css and pseudo chakra props: https://chakra-ui.com/docs/styled-system/style-props#pseudo

import pynecone as pc
from time import sleep
from email_lib import get_all_messages
from phishing_lib import get_IPQS
from tts_lib import tts
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

    def set_IPQS(self, url: str, mod_link: str):
        self.url = url
        score = get_IPQS(url)
        self.ipqs = score

        # TODO: remove this print statement
        print(f"SCORE: {score}")
        self.url_display = mod_link
        if score:
            self.risk_score = score["risk_score"]
        else:
            self.risk_score = -1

    def tts_speak(self, text: str, rate: int = 185, voice: str = "english"):
        tts(text, rate=rate, voice=voice)
        print(f"Text: {text}")


class EmailPanelState(State):
    text_color: str = "white"
    button_color_scheme: str = "orange"

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
    WELCOME_MESSAGE = "Welcome to Phission."
    PURPOSE_MESSAGE = """
        The purpose of this application is to help all users, specifically non-tech savvy individuals, 
        visually impaired individuals, et cetera., create more informed decisions as it relates to their emails. 
        Phission seeks to increase the overall awareness of Cyber Attacks. We also want to reduce the number of
        successful Cyber Attacks, primarily phishing attacks. Hence the name Phission -- Vision against Phishing
        attacks. Through this prototype, my creator hopes that you, the user, can see the value in an application
        like this. Thanks for your time and have fun!
    """
    INSTRUCTIONS_MESSAGE = """
        This application assumes that you are already logged in and are viewing your emails. By using this tool,
        you are trying to see if there are any potentially dangerous or malicious links that were sent to you via
        email. The panels below will each take you to a different email message in your inbox. Please click on one to get started.
    """
    HELP_MESSAGE = """
        Click the 'Purpose of Phission' or 'Instructions' buttons and I will share the necessary content.
    """
    return pc.center(
        pc.vstack(
            pc.divider(),
            pc.heading(
                "Welcome to Phissi👁️n!",
                font_size="5em",
                on_click=[
                    lambda: State.tts_speak(WELCOME_MESSAGE, 100),
                    lambda: State.tts_speak(PURPOSE_MESSAGE, 175),
                    lambda: State.tts_speak(
                        f"I will now read you the instructions: {INSTRUCTIONS_MESSAGE}",
                        150,
                    ),
                    lambda: State.tts_speak(
                        f"If you missed any of what I just explained, {HELP_MESSAGE}",
                        140,
                    ),
                ],
                # color="black",
                # _hover={"cursor": "pointer", "font_size": "5.1em", "color": "#f56e00"},
                color="#000000",
                _hover={"cursor": "pointer", "font_size": "5.1em", "color": "#FF7704"},
            ),
            pc.button_group(
                pc.button(
                    "Help",
                    color="white",
                    bg="#FF7704",
                    _hover={"bg": "#c25700"},
                    on_click=[
                        lambda: State.tts_speak(HELP_MESSAGE, 185),
                        lambda: State.tts_speak(
                            "You can also click on the 'Welcome to Phission' (at the top of the screen) to hear everything I have to say!",
                            175,
                        ),
                    ],
                ),
                pc.button(
                    "Purpose of Phissi👁️n",
                    color="white",
                    bg="#FF7704",
                    _hover={"bg": "#c25700"},
                    on_click=lambda: State.tts_speak(PURPOSE_MESSAGE, 175),
                ),
                pc.button(
                    "Instructions",
                    color="white",
                    bg="#FF7704",
                    _hover={"bg": "#c25700"},
                    on_click=lambda: State.tts_speak(INSTRUCTIONS_MESSAGE, 150),
                ),
                is_attached=True,
                display="flex",
            ),
            email_panel_component(EmailPanelState),
            pc.divider(),
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
