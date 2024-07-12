import studipy.browser as browser
from typing import Optional
from studipy.types import Course, Membership
from studipy.helper import safe_get
class Courses:
    def __init__(self, client):
        self._client = client
        self._auth = client._auth
        self._api_url = client._api_url
        self.me = client.me

    def get_courses(self, limit: Optional[int] = 1000) -> list[Course]:
        """returns json list of courses the user is in"""
        response = browser.get(
            self._api_url + "users/" + self.me.user_id + "/courses",
            params={"page[limit]": str(limit)},
            auth=self._auth
        )
        course_list = []
        for c in response["data"]:
            course = Course (
                    course_id=c["id"],
                    title=safe_get(c, "attributes", "title"),
                    subtitle=safe_get(c, "attributes", "subtitle"),
                    description=safe_get(c, "attributes", "description"),
                    location=safe_get(c, "attributes", "location"),
                    )
            course_list.append(course)
        return course_list

    def get_memberships(self, course: Optional[Course] = None, course_id: Optional[str] = None, limit: Optional[int] = 100000) -> list[Membership]:
        if course:
            course_id = course.course_id
        elif not course_id:
            raise ValueError("Neither course or course_id provided for get_participants")

        response = browser.get(
            self._api_url + "courses/" + course_id + "/memberships",
            params={"page[limit]": str(limit)},
            auth=self._auth
        )

        memberships = []
        for m in response["data"]:
            membership = Membership(
                    membership_id=m["id"],
                    user_id=safe_get(m, "relationships", "user", "data", "id"),
                    permission=safe_get(m, "attributes", "permission"),
                    group=safe_get(m, "attributes", "group"),
                    visible="yes",
                    label=safe_get(m, "attributes", "label")
                    )
            memberships.append(membership)

        return memberships



    def change_membership(self, updated_membership: Membership):
        _membership_id = updated_membership.membership_id
        _group = updated_membership.group
        _label = updated_membership.label
        _visible = updated_membership.visible
        data = {
                    "data": {
                        "type": "course-memberships",
                        "id": _membership_id,
                        "attributes": {
                            "group": _group,
                            "visible": _visible,
                            "label": _label
                            }
                        }
                    }

        response = browser.patch(
                url = self._api_url + "course-memberships/" + _membership_id,
                auth = self._auth,
                json = data
                )

        return response
