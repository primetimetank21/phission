# pylint: disable=no-member

import pynecone as pc
from .styles import BLACK, GREEN, ORANGE, RED, YELLOW


def score_display(
    State: pc.State,
    alert_msg: str,
    extra_tts_msg: str,
    tag: str,
    bg: str,
    status: str,
    font_color: str = "white",
):
    return pc.flex(
        pc.alert(  # high risk
            pc.icon(tag=tag, font_size="2em"),
            pc.alert_title(
                alert_msg,
                color=font_color,
                font_size="3em",
                on_click=lambda: State.tts_speak(f"{alert_msg}. {extra_tts_msg}", 140),
                _hover={"cursor": "pointer", "color": ORANGE},
            ),
            status=status,
            bg=bg,
            justify_content="center",
            width="75%",
            border_radius="15px",
            padding="5px",
            border=f"5px thin {bg}",
            height="100%",
            radius=10,
        ),
        # bg="purple",
        justify_content="center",
        align_items="center",
        height="100%",
        width="100%",
    )


def score_display_component(State: pc.State) -> pc.Component:
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
                # high risk
                score_display(
                    State=State,
                    alert_msg=alert_msg,
                    extra_tts_msg="DANGER! Please don't click this link! I believe it would be a huge mistake!",
                    tag="warning_two",
                    bg=RED,
                    status="error",
                ),
                # suspicious
                score_display(
                    State=State,
                    alert_msg=alert_msg,
                    extra_tts_msg="This link is kind of sus. VERY. SUS. I don't recommend clicking this link.",
                    tag="question",
                    bg=YELLOW,
                    status="error",
                    font_color=BLACK,
                ),
            ),
            pc.cond(
                risk_score > 0,
                # somewhat safe
                score_display(
                    State=State,
                    alert_msg=alert_msg,
                    extra_tts_msg="This link should not give you any problems. Huzzah!",
                    tag="check_circle",
                    bg=GREEN,
                    status="success",
                ),
                # error occured
                score_display(
                    State=State,
                    alert_msg="An error occured with the IPQS API (score: -1)",
                    extra_tts_msg="Click on the links at your own risk. I don't recommend it!",
                    tag="question",
                    bg=YELLOW,
                    status="error",
                    font_color=BLACK,
                ),
            ),
        ),
        pc.text("Type a URL", color="white"),
    )
