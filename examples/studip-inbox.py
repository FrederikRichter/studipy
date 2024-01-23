import studipy
from dotenv import load_dotenv
import os

load_dotenv()

username = os.getenv("STUDIP_LOGINNAME")
password = os.getenv("STUDIP_LOGINSECRET")
base_url = os.getenv("STUDIP_BASEURL")

client = studipy.Client(username=username, password=password, base_url=base_url)
messages = client.get_messages(filter_unread=True)

for m in messages["data"]:
    print(m["attributes"]["subject"])
