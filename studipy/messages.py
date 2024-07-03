import studipy.browser as browser
from studipy.types import Message, User
import requests
from typing import Optional
import json
from studipy.helper import safe_get

class Messages:
    def __init__(self, client):
        self._client = client
        self._auth = client._auth
        self._api_url = client._api_url
        self.me = client.me

    def get_messages(self, filter_unread: Optional[bool] = False, limit: Optional[int] = 100) -> list[Message]:
        """returns json list of user messages. can filter unread messages"""
        resp =  browser.get(
            self._api_url + "users/" + self.me.user_id + "/inbox",
            params={"filter[unread]": str(int(filter_unread)), "page[limit]": str(limit)},
            auth=self._auth
        )
        
        message_list = []
        for m in resp["data"]:
            message = Message(
                    message_id=m["id"],
                    subject=safe_get(m, "attributes", "subject"),
                    sender_id=safe_get(m, "relationships", "sender", "data", "id"),
                    body=safe_get(m, "attributes", "message"),
                    creation_date=safe_get(m, "attributes", "mkdate"),
                    )
            message_list.append(message)
        return message_list


    def send_message(self, message: Message, recipients: Optional[list[User]] = None, recipient_ids: Optional[list[str]] = None, priority: Optional[str] = "normal") -> requests.Response:
        """returns bytes of file content, needs specific file id"""
        if recipients:
            recipient_ids = [r.user_id for r in recipients]

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
                        "subject": message.subject,
                        "message": message.body,
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

        
    def delete_message(self, message: Optional[Message] = None, message_id = None, expected_status_code=204) -> requests.Response:
        """returns bytes of file content, needs specific file id"""
        if message:
            message_id = message.message_id

        response = browser.delete(
                url=self._api_url + "messages/" + message_id, auth=self._auth, expected_status_code=expected_status_code
                )
        return response

    def view_message(self, message: Optional[Message] = None, message_id = None) -> Message:
        """views a single message which marks it read"""
        if message:
            message_id = message.message_id

        response = browser.get(
                url=self._api_url + "messages/" + message_id, auth=self._auth
                )["data"]
        message = Message(
                message_id = response["id"],
                subject=safe_get(response, "attributes", "subject"),
                sender_id=safe_get(response, "relationships", "sender", "data", "id"),
                body=safe_get(response, "attributes", "message"),
                creation_date=safe_get(response, "attributes", "mkdate"),
                ) 
       
        return message
