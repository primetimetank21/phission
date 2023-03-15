# pylint: disable=no-member,

import pynecone as pc


def button_component(State):
    return pc.button(
        "Go Phish",
        color_scheme="green",
        on_click=State.set_IPQS,
    )
