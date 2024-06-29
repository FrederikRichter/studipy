import studipy.browser as browser
from studipy.types import User
from studipy.helper import safe_get

class Users:
    def __init__(self, client):
        self._client = client
        self._auth = client._auth
        self._api_url = client._api_url
        self.me = client.me

    def get_users(self, limit: int = 100) -> list[User]:
        """returns list of Users, length defined by limit"""
        response = browser.get(
            self._api_url + "users", params={"page[limit]": str(limit)},
            auth=self._auth
        )
        users_list = []
        for u in response["data"]:
            user = User (
                    User_id=u["id"],
                    Username=safe_get(u, "attributes", "username"),
                    E_Mail=safe_get(u, "attributes", "email"),
                    Name=safe_get(u, "attributes", "formatted-name"),
                    )
            users_list.append(user)
        return users_list
