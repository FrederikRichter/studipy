import studipy.browser as browser
from studipy.types import User
from studipy.helper import safe_get
from typing import Optional

class Users:
    def __init__(self, client):
        self._client = client
        self._auth = client._auth
        self._api_url = client._api_url
        self.me = client.me

    def get_users(self, limit: int = 100, search_q: Optional[str] = None) -> list[User]:
        """returns list of Users, length defined by limit"""
        if search_q:
            response = browser.get(
                    self._api_url + "users", params={"filter[search]": search_q},
                    auth=self._auth
                    )
        else:
            response = browser.get(
                    self._api_url + "users", params={"page[limit]": str(limit)},
                    auth=self._auth
                    )
        users_list = []
        for u in response["data"]:
            user = User (
                    user_id=u["id"],
                    username=safe_get(u, "attributes", "username"),
                    email=safe_get(u, "attributes", "email"),
                    name=safe_get(u, "attributes", "formatted-name"),
                    )
            users_list.append(user)
        return users_list
