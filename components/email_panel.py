# pylint: disable=no-member,unused-argument,unused-variable,fixme,cell-var-from-loop

import pynecone as pc
from random import choice
from .score_display import score_display_component
from .styles import BLACK, DARKENED_ORANGE, email_page_style, hstack_style, ORANGE


def clean_email_data(email_data: dict):
    email_sender = email_data["From"].split("<")
    email_sender_email = email_sender[1].replace(">", "").strip()
    email_sender_name = email_sender[0].strip().replace('"', "")

    email_receiver_email = email_data["To"]

    link_map_dict = {f"Link_{i+1}": link for (i, link) in enumerate(email_data["URLs"])}
    # print(link_map_dict)
    for link_abbreviation, link in link_map_dict.items():
        if link in email_data["Plain_Text"]:
            email_data["Plain_Text"] = email_data["Plain_Text"].replace(
                link, link_abbreviation
            )

    plain_text_modded_links = email_data["Plain_Text"]

    return (
        email_receiver_email,
        email_sender_email,
        email_sender_name,
        link_map_dict,
        plain_text_modded_links,
    )


def highlighted_links(
    State: pc.State, email_plain_text: str, link_map_dict: dict
) -> pc.Component:
    email_text_links = []
    index_pos = 0

    for short_link in link_map_dict.keys():
        short_link_pos = email_plain_text.index(short_link)

        email_text_links.append(
            pc.text(
                email_plain_text[index_pos:short_link_pos],
                as_="b",
                color=ORANGE,
                style={"white_space": "pre-line"},
            )
        )
        email_text_links.append(pc.text(short_link, as_="mark"))
        index_pos = short_link_pos + len(short_link)

    email_text_links.append(
        pc.text(
            email_plain_text[index_pos:],
            as_="b",
            color=ORANGE,
            style={"white_space": "pre-line"},
        )
    )

    return pc.center(
        pc.text(*email_text_links, font_size="2em"),
        border_radius="15px",
        padding="8px",
        border=f"5px groove {ORANGE}",
        on_click=lambda: State.tts_speak(email_plain_text),
        _hover={"cursor": "pointer", "color": ORANGE},
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
        email_receiver_email,
        email_sender_email,
        email_sender_name,
        link_map_dict,
        plain_text_modded_links,
    ) = clean_email_data(email_data)

    right_body_component = (
        no_link_email_page if email_data["URLs"] == [] else link_email_page
    )
    has_link = False if email_data["URLs"] == [] else True

    return pc.vstack(
        pc.heading(
            email_data["Subject"],
            font_size="6em",
            on_click=lambda: State.tts_speak(
                f"The email's message subject is: {email_data['Subject']}", 140
            ),
            _hover={
                "cursor": "pointer",
                "color": ORANGE,
            },
        ),
        # display component
        pc.cond(
            has_link,
            pc.cond(
                State.display_score,
                pc.flex(
                    score_display_component(State),
                    # bg="yellow",
                    width="100%",
                    height="150px",
                ),
                pc.flex(
                    pc.text(
                        "Click on a link",
                        font_size="3em",
                        align_self="start",
                        justify_self="center",
                        justify_content="center",
                        on_click=lambda: State.tts_speak("Click on a link"),
                        color="#ffffff",
                        _hover={
                            "cursor": "pointer",
                            "font_size": "3.1em",
                            "color": ORANGE,
                        },
                    ),
                    # bg="yellow",
                    width="100%",
                    # height="100%",
                    height="150px",
                    justify_content="center",
                ),
            ),
            None,
        ),
        pc.flex(
            pc.hstack(
                pc.vstack(
                    pc.text(
                        email_sender_name,
                        font_size="3em",
                        on_click=lambda: State.tts_speak(
                            f"This message sender's name is: {email_sender_name}", 140
                        ),
                        color="#ffffff",
                        _hover={
                            "cursor": "pointer",
                            "font_size": "3.1em",
                            "color": ORANGE,
                        },
                    ),
                    pc.text(
                        f"From: <{email_sender_email}>",
                        font_size="1.5em",
                        on_click=lambda: State.tts_speak(
                            f"From: <{email_sender_email}>", 140
                        ),
                        color="#ffffff",
                        _hover={
                            "cursor": "pointer",
                            "font_size": "1.6em",
                            "color": ORANGE,
                        },
                    ),
                    highlighted_links(State, plain_text_modded_links, link_map_dict),
                    # vstack styling
                    width="50vw",
                    height="100%",
                    min_height="250px",
                    padding_left="20px",
                    padding_right="20px",
                    padding_bottom="50px",
                    bg=BLACK,
                    border_radius="15px",
                    padding="5px",
                    border=f"5px thin {ORANGE}",
                    overflow="auto",
                    # flex=1,
                ),
                right_body_component(email_data, State),
                # hstack styling
                style=hstack_style,
            ),
            # flex styling
            pc.divider(),
        ),
        # vstack styling
        style=email_page_style,
    )


def no_link_email_page(email_data: dict, State: pc.State) -> pc.Component:
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
        pc.text(
            "No links found in email",
            font_size="3em",
            on_click=lambda: State.tts_speak("No links found in email. Huzzah!", 150),
            color="#ffffff",
            _hover={"cursor": "pointer", "font_size": "3.1em", "color": ORANGE},
        ),
        pc.text(" ", font_size="1.5em"),
        pc.image(
            src=chosen_gif,
            on_click=[
                lambda: State.tts_speak(
                    choice(
                        [
                            "This is a gif. I made it myself! Wink. Wink. Do you like it?",
                            "This is a gif. I made it myself! Ha ha. I'm just kidding. I didn't make it myself. Did I fool you?",
                        ]
                    ),
                    140,
                ),
                lambda: State.tts_speak(
                    "If so, please tell Dr. Washington that you liked my project! Thank you!",
                    140,
                ),
            ],
            _hover={"cursor": "pointer"},
            flex=2,
            height="100%",
        ),
        # vstack styling
        display="flex",
        align_items="center",
        justify_content="center",
        width="50vw",
        padding_left="20px",
        padding_right="20px",
        padding_bottom="50px",
        height="100%",
        min_height="250px",
        bg=BLACK,
        border_radius="15px",
        padding="5px",
        border=f"5px thin {ORANGE}",
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
        email_receiver_email,
        email_sender_email,
        email_sender_name,
        link_map_dict,
        plain_text_modded_links,
    ) = clean_email_data(email_data)

    return pc.vstack(
        pc.text(
            "Links in email",
            font_size="3em",
            on_click=lambda: State.tts_speak(
                choice(
                    [
                        "Links in email",
                        "Links in email. Hopefully nobody tried to deceive you",
                    ]
                ),
                150,
            ),
            color="#ffffff",
            _hover={"cursor": "pointer", "font_size": "3.1em", "color": ORANGE},
        ),
        pc.text(
            f"To: <{email_receiver_email}>",
            font_size="1.5em",
            on_click=lambda: State.tts_speak(
                choice(
                    [
                        f"To: <{email_receiver_email}>",
                        f"This email is to: <{email_receiver_email}>",
                    ]
                ),
                140,
            ),
            color="#ffffff",
            _hover={"cursor": "pointer", "font_size": "1.6em", "color": ORANGE},
        ),
        pc.center(
            pc.unordered_list(
                *(
                    [
                        pc.list_item(
                            pc.text(
                                *(
                                    pc.text(
                                        f"{mod_link}:",
                                        as_="mark",
                                        font_size="2em",
                                        color="#000000",
                                        _hover={
                                            "cursor": "pointer",
                                            "font_size": "2.1em",
                                            "color": ORANGE,
                                        },
                                        on_click=[
                                            lambda: State.set_IPQS(
                                                link.replace("https://", "").replace(
                                                    "http://", ""
                                                ),
                                                mod_link,
                                            ),
                                            lambda: State.tts_speak(
                                                choice(
                                                    [
                                                        f"Click the alert above if you want to hear my beautiful voice read {mod_link}'s score!",
                                                        f"Click the alert above if you want me to read {mod_link}'s score!",
                                                        " ",
                                                        " ",
                                                        " ",
                                                        " ",
                                                    ]
                                                ),
                                                140,
                                            ),
                                        ],
                                    ),
                                    pc.text(" ", as_="b", font_size="0.75em"),
                                    pc.text(
                                        link,
                                        as_="b",
                                        font_size="0.75em",
                                        style={"text_decoration": "underline"},
                                        on_click=lambda: State.tts_speak(
                                            f"{mod_link} is short for {link}", 140
                                        ),
                                        color="#ffffff",
                                        _hover={
                                            "cursor": "pointer",
                                            "font_size": "2em",
                                            "color": ORANGE,
                                        },
                                    ),
                                ),
                            )
                        )
                        for mod_link, link in link_map_dict.items()
                    ]
                ),
                # list styling
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
        # center styling
        bg=BLACK,
        border_radius="15px",
        padding="5px",
        border=f"5px thin {ORANGE}",
        height="100%",
        min_height="250px",
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
            email_route,
            title=f"Email {i}",
            route="/emails/" + str(i),
        )
    app.compile()


def get_href(i):
    return "/emails/" + i


def specific_email_panel_component(
    State: pc.State, msg: str, index: int
) -> pc.Component:
    PADDING = "20px"
    button_style = {
        "width": "95vw",
        "height": "auto",
        "padding_top": PADDING,
        "padding_bottom": PADDING,
        "variant": "solid",
    }

    return pc.link(
        pc.button(
            pc.text(msg, font_size="2em", color=State.text_color),
            # color_scheme=State.button_color_scheme,
            bg=ORANGE,
            _hover={"bg": DARKENED_ORANGE},
            style=button_style,
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
                overflow="auto",
            ),
            pc.circular_progress(
                is_indeterminate=True,
                track_color="white",
                color=ORANGE,
                thickness=15,
            ),
        ),
        height="auto",
    )
