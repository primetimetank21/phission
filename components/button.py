# pylint: disable=no-member,

import pynecone as pc


def button_component(State):
    return pc.button(
        "Go Phish",
        color="white",
        bg="#FF7704",
        _hover={"bg": "#c25700"},
        on_click=State.set_IPQS,
    )
