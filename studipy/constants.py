import studipy.browser as browser
from studipy.helper import safe_get
from studipy.types import License

def get_licenses(client) -> list[License]:
        response = browser.get(
                    url = client._api_url + "terms-of-use",
                    auth = client._auth
                )
        licenses = []
        for l in response["data"]:
            _license = License(
                        License_id = l["id"],
                        Name = safe_get(l, "attributes", "name"),
                        Description = safe_get(l, "attributes", "description")
                    )
            licenses.append(_license)
        return licenses

class Constants:
    def __init__(self, client):
        self._client = client
        self._auth = client._auth
        self._api_url = client._api_url
        self.me = client.me
        self.LICENSES = get_licenses(self._client)
