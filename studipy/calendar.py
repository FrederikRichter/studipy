import studipy.browser as browser
from studipy.helper import safe_get
from typing import Optional
from studipy.types import Schedule, Schedule_Entry

class Calendar:
    def __init__(self, client):
        self._client = client
        self._auth = client._auth
        self._api_url = client._api_url
        self.me = client.me

    def get_calendar(self) -> bytes:
        '''
        Returns calendar.ics as bytes
        '''
        return browser.download(
                url = self._api_url + "users/" + self.me.user_id + "/events.ics",
                auth=self._auth
                )

    def get_schedule(self) -> Schedule:
        '''
        Returns Schedule type with Entries from current semester
        '''
        response =  browser.get(
                self._api_url + "users/" + self.me.user_id + "/schedule",
                auth=self._auth
                )
        entry_list = []
        for e in response.get("data", {}):
            entry = Schedule_Entry(
                    entry_id = e["id"],
                    title = safe_get(e, "attributes", "title"),
                    description = safe_get(e, "attributes", "description"),
                    start = safe_get(e, "attributes", "start"),
                    end = safe_get(e, "attributes", "end"),
                    frequency = safe_get(e, "attributes", "recurrence", "FREQ"),
                    related_course_id = safe_get(e, "relationships", "owner", "data", "id")
                    )
            entry_list.append(entry)

        schedule = Schedule(
                    entries = entry_list
                )

        return schedule
