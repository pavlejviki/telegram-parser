import pandas as pd
from telethon.errors import SessionPasswordNeededError
from telethon.sync import TelegramClient
import csv
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, PeerChannel, ChannelParticipantsSearch



api_id = 18377495
api_hash = 'a0c785ad0fd3e92e7c131f0a70987987'
phone = 'ваш номер телефона, привязанный к профилю'

client = TelegramClient(phone, api_id, api_hash)
client.start()