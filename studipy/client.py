import studipy.browser as browser
from studipy.courses import Courses
from studipy.messages import Messages
from studipy.files import Files
from studipy.constants import Constants
from studipy.users import Users
from studipy.helper import safe_get
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
        _v_res = browser.get(
                    url=self._api_url + "studip/properties",
                    auth=self._auth
                )
        self.version = None
        for p in _v_res["data"]:
            if "studip-version" in p.values():
               self.version = safe_get(p, "attributes", "value")
               break
        _tested_version = "6.0.alpha"
        if self.version != _tested_version:
            print(f"""
                  WARNING: This library was tested on version {_tested_version} and does not match your version {self.version}.
                  You might encounter Bugs that have been fixed in newer Versions of Studip.
                  Ask your Administrator to update the JSONAPI if it does not match the newest Version found on 
                  https://gitlab.studip.de/groups/studip/-/milestones?sort=name_desc
                  """)
        _u_res = browser.get(self._api_url + "users/me",
                           auth=self._auth
                           )["data"]
        self.me = User(
                user_id = _u_res["id"],
                username = safe_get(_u_res, "attributes", "username"),
                name = safe_get(_u_res, "attributes", "formatted-name"),
                email = safe_get(_u_res, "attributes", "email")
                )
        self.Courses = Courses(client=self)
        self.Messages = Messages(client=self)
        self.Files = Files(client=self)
        self.Constants = Constants(client=self)
        self.Users = Users(client=self)
