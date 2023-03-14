# type: ignore
# pylint: disable=no-member, fixme

import pynecone as pc
from phishing_lib import get_IPQS
from .styles import app_style, input_style, container_style


# State
class State(pc.State):
    """The app state."""

    url: str = ""
    url_display: str = ""
    risk_score: int = None

    # TODO: extract more values from this in set_IPQS
    ipqs: dict = {}
    # is_suspicious: bool

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
        score = get_IPQS(url)
        self.ipqs = score

        # TODO: remove this print statement
        print(score)
        if score:
            self.url_display = url
            self.risk_score = score["risk_score"]


# Components
def score_display_component() -> pc.Component:
    # risk_icon = get_risk_icon()

    alert_msg = (
        '"'
        + State.url_display
        + '" is a '
        + State.get_risk_str
        + " website! (score: "
        + State.risk_score
        + ")"
    )

    risk_score = State.risk_score

    return pc.cond(
        State.display_score,
        pc.cond(  # for unsafe vs somewhat safe
            risk_score >= 75,
            pc.cond(  # for high risk vs suspicious
                risk_score >= 85,
                pc.alert(  # high risk
                    pc.icon(tag="warning_two"),
                    pc.alert_title(alert_msg, color="white"),
                    status="error",
                    bg="#0051a8",
                ),
                pc.alert(  # suspicious
                    pc.icon(tag="question"),
                    pc.alert_title(alert_msg, color="white"),
                    status="error",
                    bg="#0051a8",
                ),
            ),
            pc.alert(  # somewhat safe
                pc.icon(tag="check_circle"),
                pc.alert_title(alert_msg, color="white"),
                status="error",
                bg="#0051a8",
            ),
        ),
        pc.text("Type a URL", color="white"),
    )


def input_component() -> pc.Component:
    return pc.container(
        pc.input(
            on_blur=State.set_url,
            placeholder="Url to test (i.e., google.com)",
            style=input_style,
            focus_border_color="None",
        ),
        # container settings
        style=container_style,
    )


def button_component():
    return pc.button(
        "Go Phish",
        color_scheme="green",
        on_click=State.set_IPQS,
    )


def index() -> pc.Component:
    return pc.center(
        pc.vstack(
            pc.heading("Welcome to Phissi👁️n!", font_size="2em"),
            score_display_component(),
            input_component(),
            button_component(),
            spacing="1.5em",
            font_size="2em",
        ),
        # vstack formatting
        style=app_style,
    )


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index)
app.compile()
