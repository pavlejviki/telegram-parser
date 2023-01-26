import os

import pandas as pd
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PHONE = os.getenv("PHONE")

client = TelegramClient(PHONE, int(API_ID), API_HASH)
client.start()


def create_html_table(data: list, columns: list) -> str:
    """
    Creates an HTML table from a list of data and a list of column names.
    """
    df = pd.DataFrame(
        data,
        columns=columns,
    )
    html_table = df.to_html(index=False)
    return html_table


def save_to_file(title: str, table: str) -> None:
    """
    Saves an HTML table to a file with the specified name.
    """
    with open(f"{title}-members.html", "w", encoding="UTF-8") as f:
        f.write(table)
    print("You file with user's data is ready.")


async def parse_users():
    """
    Asynchronously parses users from a Telegram channel specified by the user.
    """
    channel = input(
        "Please enter the link to the channel you want to parse the users from:"
    )
    print("Parsing, please wait...")
    target_channel = await client.get_entity(channel)
    offset = 0
    limit = 1000
    all_participants = []
    while True:
        participants = await client(
            GetParticipantsRequest(
                target_channel, ChannelParticipantsSearch(""), offset, limit, hash=0
            )
        )
        if not participants.users:
            break
        all_participants.extend(participants.users)
        offset += len(participants.users)

    all_user_details = []
    for participant in all_participants:
        user_id = participant.id
        first_name = participant.first_name
        last_name = participant.last_name
        user_name = participant.username
        phone = participant.phone
        all_user_details.append([user_id, first_name, last_name, user_name, phone])

    html_table = create_html_table(
        all_user_details, ["id", "First name", "Last name", "User name", "Phone"]
    )
    save_to_file(target_channel.title, html_table)


with client:
    client.loop.run_until_complete(parse_users())
