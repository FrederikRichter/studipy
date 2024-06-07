import studipy.browser as browser
from typing import Any

class Client:
    def __init__(self, username: str, password: str, base_url: str) -> None:
        """Init studipy Client.
        Keyword arguments:
        username -- the studIP username (like normal login)
        password -- the studIP password (...)
        base url -- studIP instancce base url (https://studip.example.com/)
        """
        self._auth: tuple[str, str] = (username, password)
        self._api_url: str = f'{base_url}jsonapi.php/v1/'
        self.me: Any = browser.get(self._api_url + "users/me", auth=self._auth)

    def get_courses(self) -> Any:
        """returns json list of courses the user is in"""
        return browser.get(
            self._api_url + "users/" + self.me["data"]["id"] + "/courses",
            params={"page[limit]": "-1"},
            auth=self._auth
        )

    def get_semesters(self) -> Any:
        """returns json list of semesters"""
        return browser.get(
            self._api_url + "semesters",
            auth=self._auth
        )
    
    def get_calender_ics(self) -> bytes:
        """returns user calendar in ics format"""
        return browser.download(
            self._api_url + "users/" + self.me["data"]["id"] + "/events.ics",
            auth=self._auth
        )

    def view_course(self, course_id: str) -> Any:
        """returns json data about a specific course, need course id"""
        return browser.get(
            self._api_url + "courses/" + course_id,
            auth=self._auth
        )

    def get_course_folders(self, course_id: str) -> Any:
        """returns json list of folders inside a specific course, needs course id"""
        return browser.get(
            self._api_url + "courses/" + course_id + "/folders",
            auth=self._auth
        )

    def get_course_files(self, course_id: str) -> Any:
        """returns json list of file refs in a specific course, needs course id"""
        return browser.get(
            self._api_url + "courses/" + course_id + "/file-refs",
            auth=self._auth
        )

    def get_subfolders(self, folder_id: str) -> Any:
        """returns json list of folders inside a specific folder, needs folder id"""
        return browser.get(
            self._api_url + "folders/" + folder_id + "/folders",
            auth=self._auth
        )

    def get_folder_files(self, folder_id: str) -> Any:
        """returns json list of file refs in a specific folder, needs folder id"""
        return browser.get(
            self._api_url + "folders/" + folder_id + "/file-refs",
            auth=self._auth
        )

    def get_users(self, limit: int = 30) -> Any:
        """returns json list of userdata
        Keyword arguments:
        limit -- the max amount of users listed. limit of -1 lists all
        """
        return browser.get(
            self._api_url + "users", params={"page[limit]": str(limit)},
            auth=self._auth
        )

    def get_messages(self, filter_unread: bool = False) -> Any:
        """returns json list of user messages. can filter unread messages"""
        return browser.get(
            self._api_url + "users/" + self.me["data"]["id"] + "/inbox",
            params={"filter[unread]": str(int(filter_unread))},
            auth=self._auth
        )

    def download_file(self, file_id: str) -> bytes:
        """returns bytes of file content, needs specific file id"""
        return browser.download(
            self._api_url + "file-refs/" + file_id + "/content", auth=self._auth
        )
