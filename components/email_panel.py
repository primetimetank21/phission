# pylint: disable=no-member,

import pynecone as pc


def email_ui(email_data: dict) -> pc.Component:
    return pc.vstack(
        pc.text(email_data["From"]),
        pc.text(email_data["To"]),
        pc.text(email_data["Date"]),
        pc.text(email_data["Subject"]),
        pc.text(email_data["Plain_Text"]),
        pc.text(email_data["URLs"]),
        display="flex",
        align_items="center",
        justify_content="center",
    )


def get_email_page_route(email_dict: dict) -> pc.Component:
    def email_page() -> pc.Component:
        return email_ui(email_dict)

    return email_page


def get_href(i):
    return "/emails/" + i


def specific_email_panel_component(
    State: pc.State, msg: str, index: int
) -> pc.Component:
    PADDING = "20px"

    return pc.link(
        pc.button(
            pc.text(msg, font_size="2em", color=State.text_color),
            width="95vw",
            height="auto",
            padding_top=PADDING,
            padding_bottom=PADDING,
            variant="solid",
            color_scheme=State.button_color_scheme,
            # on_click=lambda: State.get_email_by_subject_index(index),
        ),
        href=get_href(index),
        is_external=True,
    )


def email_panel_component(State: pc.State) -> pc.Component:
    return pc.vstack(
        pc.cond(
            State.display_email_message_subjects,
            pc.foreach(
                State.email_message_subjects,
                lambda msg, index: specific_email_panel_component(  # pylint: disable=unnecessary-lambda
                    State, msg, index
                ),
            ),
            pc.circular_progress(
                is_indeterminate=True,
                track_color="white",
                color="green",
                thickness=15,
            ),
        ),
        height="auto",
    )
