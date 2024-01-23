import studipy.browser as browser


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
        self.me = browser.get(self._api_url + "users/me", auth=self._auth)

    def get_courses(self) -> object:
        """returns json list of courses the user is in"""
        return browser.get(
            self._api_url + "users/" + self.me + "/courses/",
            params={"page[limit]": "-1"},
            auth=self._auth
        )

    def view_course(self, course_id) -> object:
        """returns json data about a specific course, need course id"""
        return browser.get(
            self._api_url + "courses/" + course_id,
            auth=self._auth
        )

    def get_course_folders(self, course_id) -> object:
        """returns json list of folders inside a specific course, needs course id"""
        return browser.get(
            self._api_url + "courses/" + course_id + "/folders",
            auth=self._auth
        )

    def get_course_files(self, course_id) -> object:
        """returns json list of file refs in a specific course, needs course id"""
        return browser.get(
            self._api_url + "courses/" + course_id + "/file-refs",
            auth=self._auth
        )

    def get_subfolders(self, folder_id) -> object:
        """returns json list of folders inside a specific folder, needs folder id"""
        return browser.get(
            self._api_url + "folders/" + folder_id + "/folders",
            auth=self._auth
        )

    def get_folder_files(self, folder_id) -> object:
        return browser.get(
            self._api_url + "folders/" + folder_id + "/file-refs",
            auth=self._auth
        )

    def get_users(self, limit=30) -> object:
        """returns json list of userdata
        Keyword arguments:
        limit -- the max amount of users listed. limit of -1 lists all
        """
        return browser.get(
            self._api_url + "users", params={"page[limit]": str(limit)},
            auth=self._auth
        )

    def get_messages(self, filter_unread=False) -> object:
        """returns json list of user messages. can filter unread messages"""
        return browser.get(
            self._api_url + "users/" + self.me["data"]["id"] + "/inbox",
            params={"filter[unread]": str(int(filter_unread))},
            auth=self._auth
        )

    def download_file(self, file_id) -> bytes:
        """returns bytes of file content, needs specific file id"""
        return browser.download(
            self._api_url + "file-refs/" + file_id + "/content", auth=self._auth
        )

