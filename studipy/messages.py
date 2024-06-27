import studipy.browser as browser
from studipy.types import Message

class Messages:
    def __init__(self, client):
        self._client = client
        self._auth = client._auth
        self._api_url = client._api_url
        self.me = client.me

    def get_messages(self, filter_unread=False) -> object:
        """returns json list of user messages. can filter unread messages"""
        resp =  browser.get(
            self._api_url + "users/" + self.me.User_id + "/inbox",
            params={"filter[unread]": str(int(filter_unread))},
            auth=self._auth
        )
        
        message_list = []
        for m in resp["data"]:
            message = Message(
                    Message_id=m["id"],
                    Title=m["attributes"].get("subject", None),
                    Sender_id=m["relationships"].get("sender", {}).get("data", {}).get("id", None),
                    Body=m["attributes"].get("message", None),
                    Creation_Date=m["attributes"]["mkdate"],
                    )
            message_list.append(message)
        return message_list
