# pylint: disable=no-member,unused-argument,unused-variable,fixme

import pynecone as pc
from random import choice
from .styles import email_page_style, hstack_style


def clean_email_data(email_data: dict):
    # print(f"email_data['From']: {email_data['From']}")
    email_sender = email_data["From"].split("<")
    # print(f"email_sender: {email_sender}")
    email_sender_email = email_sender[1].replace(">", "").strip()
    email_sender_name = email_sender[0].strip().replace('"', "")  # .split(",")
    # email_sender_name = f"{email_sender_name[1]} {email_sender_name[0]}"

    link_map_dict = {f"Link_{i+1}": link for i, link in enumerate(email_data["URLs"])}
    for link_abbreviation, link in link_map_dict.items():
        if link in email_data["Plain_Text"]:
            email_data["Plain_Text"] = email_data["Plain_Text"].replace(
                link, link_abbreviation
            )
    plain_text_modded_links = email_data["Plain_Text"]
    return (
        email_sender_email,
        email_sender_name,
        link_map_dict,
        plain_text_modded_links,
    )


def highlighted_links(email_plain_text: str, link_map_dict: dict) -> pc.Component:
    email_text_links = []
    index_pos = 0

    for key in link_map_dict.keys():
        key_pos = email_plain_text.index(key)
        email_text_links.append(pc.text(email_plain_text[index_pos:key_pos], as_="b"))
        email_text_links.append(
            pc.text(key, as_="mark")
        )  # TODO: maybe make this a link (if it's safe)
        index_pos = key_pos + len(key)

    email_text_links.append(pc.text(email_plain_text[index_pos:], as_="b"))

    return pc.center(
        pc.text(*email_text_links, font_size="2em"),
        border_radius="15px",
        border_width="thick",
    )


def email_page_skeleton(email_data: dict, State: pc.State) -> pc.Component:
    """
    pc.text(email_data["From"]),
    pc.text(email_data["To"]),
    pc.text(email_data["Date"]),
    pc.text(email_data["Subject"]),
    pc.text(email_data["Plain_Text"]),
    pc.text(email_data["URLs"]),
    """

    # clean up email_data
    (
        email_sender_email,
        email_sender_name,
        link_map_dict,
        plain_text_modded_links,
    ) = clean_email_data(email_data)
    # print(rf"{plain_text_modded_links}")
    body_component = no_link_email_page if email_data["URLs"] == [] else link_email_page

    return pc.vstack(
        pc.heading(email_data["Subject"], font_size="6em"),
        pc.center(
            pc.hstack(
                pc.vstack(
                    pc.text(email_sender_name, font_size="3em"),
                    pc.text(f"<{email_sender_email}>", font_size="1.5em"),
                    highlighted_links(plain_text_modded_links, link_map_dict),
                    # vstack styling
                    width="50vw",
                    padding_left="20px",
                    padding_right="20px",
                    bg="green",
                    # flex=1,
                ),
                body_component(email_data, State),
                # hstack styling
                style=hstack_style,
            ),
            # center styling
        ),
        # vstack styling
        style=email_page_style,
    )


def no_link_email_page(email_data: dict, State: pc.State) -> pc.Component:
    # clean up email_data
    # email_sender_email, email_sender_name, link_map_list, plain_text_modded_links = clean_email_data(email_data)
    emotional_gifs = [
        "https://media.tenor.com/FKlml5CuZCEAAAAC/purple-banana-syndicate-pbs.gif",
        "https://www.icegif.com/wp-content/uploads/2022/10/icegif-1341.gif",
        "https://fcit.usf.edu/matrix/wp-content/uploads/2017/01/DanceBot-3-Med.gif",
        "https://gifdb.com/images/thumbnail/happy-dance-qoobee-dragon-h8cge3ua7c4kmua2.gif",
        "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExOGJjZTVlZmYxN2I0YjIzYTQwYzE2ZDBjOThkMTZjOTIwZGMzNzAwZCZlcD12MV9pbnRlcm5hbF9naWZzX2dpZklkJmN0PXM/AFmZwgpOXOqWwtcVve/giphy.gif",
        "https://gifdb.com/images/file/happy-snoop-dogg-party-5uvm2sf7xnxnhlep.gif",
    ]
    chosen_gif = choice(emotional_gifs)
    return pc.vstack(
        pc.text("No links found in email", font_size="3em"),
        pc.image(
            src=chosen_gif,
            # src=emotional_gifs[-1],
        ),
        # vstack styling
        display="flex",
        align_items="center",
        justify_content="center",
        width="50vw",
        padding_left="20px",
        padding_right="20px",
        bg="purple",
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
    (
        email_sender_email,
        email_sender_name,
        link_map_list,
        plain_text_modded_links,
    ) = clean_email_data(email_data)

    return pc.vstack(
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
    )


def email_ui(email_data: dict, State: pc.State) -> pc.Component:
    return email_page_skeleton(email_data, State)


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
