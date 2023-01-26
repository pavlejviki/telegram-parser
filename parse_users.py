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

if client.is_connected():
    print("Client is connected")
else:
    print("Client is not connected, check your credentials.")


async def parse_users():
    channel = input("Please enter the link to the channel you want to parse the users from:")
    print("Parsing, please wait...")
    target_channel = await client.get_entity(channel)
    offset = 0
    limit = 1000
    all_participants = []
    while True:
        participants = await client(GetParticipantsRequest(
            target_channel, ChannelParticipantsSearch(''), offset, limit,
            hash=0
        ))
        if not participants.users:
            break
        all_participants.extend(participants.users)
        offset += len(participants.users)

    all_user_details = []
    for participant in all_participants:
        id = participant.id
        first_name = participant.first_name
        last_name = participant.last_name
        user_name = participant.username
        phone = participant.phone
        all_user_details.append([id, first_name, last_name, user_name, phone])

    df = pd.DataFrame(all_user_details, columns=["id", "First name", "Last name", "User name", "Phone"])
    html_table = df.to_html(index=False)

    with open(f"{target_channel.title}-members.html", "w", encoding="UTF-8") as f:
        f.write(html_table)
    print("You file with user's data is ready.")


with client:
    client.loop.run_until_complete(parse_users())
