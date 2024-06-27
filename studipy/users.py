import studipy.browser as browser
from studipy.types import User, Course

class Users:
    def __init__(self, client):
        self._client = client
        self._auth = client._auth
        self._api_url = client._api_url
        self.me = client.me

    def get_courses(self) -> list[Course]:
        """returns json list of courses the user is in"""
        response = browser.get(
            self._api_url + "users/" + self.me.User_id + "/courses",
            params={"page[limit]": "-1"},
            auth=self._auth
        )
        course_list = []
        for c in response["data"]:
            course = Course (
                    Course_id = c["id"],
                    Title = c["attributes"]["title"],
                    Subtitle = c["attributes"]["subtitle"],
                    Description = c["attributes"]["description"],
                    Location = c["attributes"]["location"]
                    )
            course_list.append(course)
        return course_list

    # def get_participants(self, course: Course) -> list[User]:
    #     response = browser.get(
    #         self._api_url + "users/" + self.me["User_id"] + "/courses",
    #         params={"page[limit]": "-1"},
    #         auth=self._auth
    #     )
