import os

from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from dotenv import load_dotenv

from utils import create_html_table, save_to_file

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PHONE = os.getenv("PHONE")

client = TelegramClient(PHONE, int(API_ID), API_HASH)
client.start()


async def parse_messages() -> None:
    """
    Asynchronously parses messages from a Telegram channel specified by the user.
    Use total_count_limit variable to set the number of messages you want to parse
    in case you don't want all of them or parsing all takes too much time
    (if set to 0 all messages will be parsed).
    """
    channel = input(
        "Please enter the link to the channel you want to parse the messages from:"
    )
    print("Parsing, please wait...")
    target_channel = await client.get_entity(channel)

    offset_id = 0
    limit = 100
    all_messages = []
    total_count_limit = 1000

    while True:
        history = await client(
            GetHistoryRequest(
                peer=target_channel,
                offset_id=offset_id,
                offset_date=None,
                add_offset=0,
                limit=limit,
                max_id=0,
                min_id=0,
                hash=0,
            )
        )
        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            message_id = message.id
            text = message.message
            sender = message.from_id
            date = message.date
            all_messages.append([message_id, text, sender, date])
        offset_id = messages[len(messages) - 1].id
        total_messages = len(all_messages)
        if total_count_limit != 0 and total_messages >= total_count_limit:
            break

    html_table = create_html_table(
        all_messages, ["id", "Text", "Sender", "Date"]
    )
    save_to_file(target_channel.title, html_table, "messages")


with client:
    client.loop.run_until_complete(parse_messages())
