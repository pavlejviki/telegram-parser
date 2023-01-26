import os
import pandas as pd
from telethon import TelegramClient
from telethon.tl.functions.messages import (GetHistoryRequest)

from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PHONE = os.getenv("PHONE")

client = TelegramClient(PHONE, int(API_ID), API_HASH)
client.start()


async def main():
    channel = input("Please enter the link to the channel you want to parse the messages from:")
    print("Parsing, please wait...")
    target_channel = await client.get_entity(channel)

    offset_id = 0
    limit = 1000
    all_messages = []

    while True:
        history = await client(GetHistoryRequest(
            peer=target_channel,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))
        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            id = message.id
            text = message.message
            sender = message.from_id
            receiver = message.to_id
            date = message.date
            all_messages.append([id, text, sender, receiver, date])
        offset_id = messages[len(messages) - 1].id

    df = pd.DataFrame(all_messages, columns=["id", "Text", "Sender", "Receiver", "Date"])
    html_table = df.to_html(index=False)

    with open(f"{target_channel.title}-messages.html", "w", encoding="UTF-8") as f:
        f.write(html_table)
    print("You file with message data is ready.")


with client:
    client.loop.run_until_complete(main())
