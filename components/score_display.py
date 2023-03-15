# pylint: disable=no-member

import pynecone as pc


def score_display_component(State) -> pc.Component:
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
