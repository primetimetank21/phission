# pylint: disable=no-member

import pynecone as pc
from .styles import input_style, container_style


def input_component(State) -> pc.Component:
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
