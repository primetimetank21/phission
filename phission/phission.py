# type: ignore
# pylint: disable=no-member, fixme

# TODO: connect Gmail API

import pynecone as pc
from phishing_lib import get_IPQS
from .styles import app_style
from components import button_component, score_display_component, input_component


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


def index() -> pc.Component:
    return pc.center(
        pc.vstack(
            pc.heading("Welcome to Phissi👁️n!", font_size="2em"),
            score_display_component(State),
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
app.add_page(index)
app.compile()
