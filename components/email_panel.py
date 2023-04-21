# pylint: disable=no-member,unused-argument,unused-variable

import pynecone as pc
from .styles import email_page_style


def clean_email_data(email_data: dict):
    print(f"email_data['From']: {email_data['From']}")
    email_sender = email_data["From"].split("<")
    print(f"email_sender: {email_sender}")
    email_sender_email = email_sender[1].replace(">", "").strip()
    email_sender_name = email_sender[0].strip().replace('"', "")  # .split(",")
    # email_sender_name = f"{email_sender_name[1]} {email_sender_name[0]}"
    return (email_sender_email, email_sender_name)


def no_link_email_page(email_data: dict, State: pc.State) -> pc.Component:
    # clean up email_data
    email_sender_email, email_sender_name = clean_email_data(email_data)

    return pc.vstack(
        pc.heading(email_data["Subject"]),
        pc.hstack(
            pc.vstack(
                pc.text(email_sender_name),
                pc.text(email_data["Plain_Text"]),  # message content
                # vstack styling
                width="50vw",
                # padding_left="20px",
                # padding_right="20px",
                bg="green",
                flex=1,
            ),
            pc.vstack(
                pc.text("No links"),
                pc.image(
                    src="https://www.icegif.com/wp-content/uploads/2022/10/icegif-1341.gif",
                ),
                # vstack styling
                display="flex",
                align_items="center",
                justify_content="center",
                width="50vw",
                # padding_left="20px",
                # padding_right="20px",
                bg="purple",
                flex=1,
            ),
            # hstack styling
            display="flex",
            align_items="start",
            justify_content="center",
            bg="red",
            flex=1,
        ),
        # vstack styling
        display="flex",
        align_items="center",
        justify_content="start",
        style=email_page_style,
        flex=1,
    )


def link_email_page(email_data: dict, State: pc.State) -> pc.Component:
    """
    pc.text(email_data["From"]),
    pc.text(email_data["To"]),
    pc.text(email_data["Date"]),
    pc.text(email_data["Subject"]),
    pc.text(email_data["Plain_Text"]),
    pc.text(email_data["URLs"]),
    """
    # clean up email_data
    email_sender_email, email_sender_name = clean_email_data(email_data)

    return pc.vstack(
        pc.heading(email_data["Subject"]),
        pc.hstack(
            pc.vstack(
                pc.text(email_sender_name),
                pc.text(email_data["Plain_Text"]),  # message content
                # vstack styling
                flex=1,
                width="50vw",
                padding_left="20px",
                padding_right="20px",
            ),
            pc.vstack(
                pc.unordered_list(
                    *([pc.list_item(url) for url in email_data["URLs"]]),
                    # list styling
                    # display="flex",
                    # align_items="center",
                    # justify_content="center",
                    spacing=".25em",
                    flex=1,
                ),
                # vstack styling
                display="flex",
                align_items="center",
                justify_content="center",
                width="50vw",
                padding_left="20px",
                padding_right="20px",
            ),
            # hstack styling
            display="flex",
            align_items="center",
            justify_content="center",
        ),
        # vstack styling
        display="flex",
        align_items="center",
        justify_content="center",
        style=email_page_style,
    )


def email_ui(email_data: dict, State: pc.State) -> pc.Component:
    if email_data["URLs"] == []:
        return no_link_email_page(email_data, State)

    return link_email_page(email_data, State)


def get_email_page_route(email_dict: dict, app_state: pc.State) -> pc.Component:
    def email_page() -> pc.Component:
        return email_ui(email_dict, app_state)

    return email_page


# pylint: disable=fixme
def set_email_page_routes(emails, app):
    for i, email in enumerate(emails):
        email_route = get_email_page_route(email, app.state)
        app.add_page(
            email_route, title=f"Email {i}", route="/emails/" + str(i)
        )  # TODO: add on_load => run get_IPQS on each URL (if any) using asyncio
    app.compile()


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
