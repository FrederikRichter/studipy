import studipy.browser as browser
from studipy.types import Message, User
import requests
from typing import Optional
import json

class Messages:
    def __init__(self, client):
        self._client = client
        self._auth = client._auth
        self._api_url = client._api_url
        self.me = client.me

    def get_messages(self, filter_unread: Optional[bool] = False, limit: Optional[int] = 100) -> list[Message]:
        """returns json list of user messages. can filter unread messages"""
        resp =  browser.get(
            self._api_url + "users/" + self.me.User_id + "/inbox",
            params={"filter[unread]": str(int(filter_unread)), "page[limit]": str(limit)},
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


    def send_message(self, message: Message, recipients: Optional[list[User]] = None, recipient_ids: Optional[list[str]] = None, priority: Optional[str] = "normal") -> requests.Response:
        """returns bytes of file content, needs specific file id"""
        if recipients:
            recipient_ids = [r.User_id for r in recipients]

        headers = {
                'Content-Type': 'application/vnd.api+json',
                }
       
        recipients_data = []
        for r in recipient_ids:
            recipients_data.append({
                "type": "users",
                "id": r
                })

        data = {
                "data": {
                    "type": "messages",
                    "attributes": {
                        "subject": message.Title,
                        "message": message.Body,
                        "priority": priority
                        },
                    "relationships": {
                        "recipients": {
                            "data": recipients_data
                            }
                        }
                    }
                }
       
        response = browser.post(
                url=self._api_url + "messages",
                auth=self._auth,
                data=json.dumps(data),
                headers=headers
                )

        return response
