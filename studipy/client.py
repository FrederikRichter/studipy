import studipy.browser as browser


class Client:
    def __init__(self, username, password, base_url):
        self._auth = (username, password)
        self._api_url = f'{base_url}jsonapi.php/v1/'
        self.me = browser.get(self._api_url + "users/me", auth=self._auth)

    def get_courses(self) -> object:
        return browser.get(
            self._api_url + "users/" + self.me + "/courses/",
            params={"page[limit]" : "-1"},
            auth=self._auth
            )
    
    def view_course(self, course_id) -> object:
        return browser.get(
            self._api_url + "courses/" + course_id,
            auth=self._auth
            )
    
    def get_course_folders(self, course_id) -> object:
        return browser.get(
            self._api_url + "courses/" + course_id + "/folders",
            auth=self._auth
            )
    
    def get_course_files(self, course_id) -> object:
        return browser.get(
            self._api_url + "courses/" + course_id + "/file-refs",
            auth=self._auth
            )
    
    def get_subfolders(self, folder_id) -> object:
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
        return browser.get(
            self._api_url + "users", params={"page[limit]" : limit},
            auth=self._auth
            )
    
    def get_messages(self, filter_unread=0) -> object:
        return browser.get(
            self._api_url + "users/" + self.me + "/inbox",
            params={"filter[unread]" : str(filter_unread)},
            auth=self._auth
            )
    
    def download_file(self, file_id) -> bytes:
        return browser.download(
            self._api_url + "file-refs/" + file_id + "/content", auth=self._auth
            )