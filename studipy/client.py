import studipy.browser as browser
from studipy.courses import Courses
from studipy.messages import Messages
from studipy.file_handler import File_Handler
from studipy.constants import Constants
from studipy.users import Users

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
        self.Constants = Constants(client=self)
        self.Users = Users(client=self)
