# type: ignore
# pylint: disable=no-member
"""Welcome to Pynecone! This file outlines the steps to create a basic app."""
from pcconfig import config

import pynecone as pc

docs_url = "https://pynecone.io/docs/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"


class State(pc.State):
    """The app state."""

    url: str = "goalgoof.com"
    risk_score: int = 92
    search_text: str = ""


def index() -> pc.Component:
    return pc.center(
        pc.vstack(
            pc.alert(
                pc.alert_icon(),
                pc.alert_title(
                    '"'
                    + State.url
                    + '" is a risky website! (score: '
                    + State.risk_score
                    + ")"
                ),
                status="error",
            ),
            pc.heading("Welcome to Phissi👁️n!", font_size="2em"),
            pc.input(
                on_blur=State.set_search_text,
                placeholder="Url to test (i.e., google.com)",
            ),
            pc.button("Go Phish", color_scheme="green"),
            spacing="1.5em",
            font_size="2em",
        ),
        padding_top="10%",
    )


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index)
app.compile()
