import studipy
from studipy.types import Message
from dotenv import load_dotenv
import os

load_dotenv()

username = os.getenv("STUDIP_LOGINNAME")
password = os.getenv("STUDIP_LOGINSECRET")
base_url = os.getenv("STUDIP_BASEURL")

client = studipy.Client(username=username, password=password, base_url=base_url)
messages: list[Message] = client.Messages.get_messages(filter_unread=True)

# print message subjects
for m in messages:
    print(m.subject)
