# pylint: disable=no-member

import pynecone as pc


def score_display(
    State: pc.State,
    alert_msg: str,
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
                font_size="2em",
            ),
            status=status,
            # bg="#0051a8", #blue
            bg=bg,  # sumn else
            align_self="start",
            justify_self="center",
            justify_content="center",
            radius=10,
            on_click=lambda: State.tts_speak(alert_msg, 140),
            _hover={"cursor": "pointer"},
        ),
        bg="purple",
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
                    tag="warning_two",
                    bg="#05abc3",
                    status="error",
                ),
                # suspicious
                score_display(
                    State=State,
                    alert_msg=alert_msg,
                    tag="question",
                    bg="yellow",
                    status="error",
                    font_color="black",
                ),
            ),
            pc.cond(
                risk_score > 0,
                # somewhat safe
                score_display(
                    State=State,
                    alert_msg=alert_msg,
                    tag="check_circle",
                    bg="green",
                    status="success",
                ),
                # error occured
                score_display(
                    State=State,
                    alert_msg="An error occured with the IPQS API (score: "
                    + State.risk_score
                    + ")",
                    tag="question",
                    bg="yellow",
                    status="error",
                    font_color="black",
                ),
            ),
        ),
        pc.text("Type a URL", color="white"),
    )
