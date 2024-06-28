import studipy.browser as browser
from studipy.courses import Courses
from studipy.messages import Messages
from studipy.file_handler import File_Handler

from studipy.types import User

class Client:
    def __init__(self, username, password, base_url):
        """Init studipy Client.
        Keyword arguments:
        username -- the studIP username (like normal login)
        password -- the studIP password (...)
        base url -- studIP instancce base url (https://studip.example.com/)
        """
        self._auth = (username, password)
        self._api_url = f'{base_url}jsonapi.php/v1/'
        _res = browser.get(self._api_url + "users/me", auth=self._auth)["data"]
        self.me = User(
                User_id = _res["id"],
                Username = _res["attributes"]["username"],
                Name = _res["attributes"]["formatted-name"],
                E_Mail = _res["attributes"]["email"]
                )
        self.Courses = Courses(client=self)
        self.Messages = Messages(client=self)
        self.File_Handler = File_Handler(client=self)
    #
    # def get_users(self, limit=30) -> object:
    #     """returns json list of userdata
    #     Keyword arguments:
    #     limit -- the max amount of users listed. limit of -1 lists all
    #     """
    #     return browser.get(
    #         self._api_url + "users", params={"page[limit]": str(limit)},
    #         auth=self._auth
    #     )
    #
    # def download_file(self, file_id) -> bytes:
    #     """returns bytes of file content, needs specific file id"""
    #     return browser.download(
    #         self._api_url + "file-refs/" + file_id + "/content", auth=self._auth
    #     )

