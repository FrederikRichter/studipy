import studipy.browser as browser
from studipy.types import Folder, File, Course, File_Metadata
from studipy.helper import safe_get
from typing import Optional

class File_Handler:
    def __init__(self, client):
        self._client = client
        self._auth = client._auth
        self._api_url = client._api_url
        self._me = client.me

    def get_folders(self, course: Optional[Course] = None, folder: Optional[Folder] = None) -> list[Folder]:
        """returns list of Folders in a course"""
        if course:
            response = browser.get(
                self._api_url + "courses/" + course.Course_id + "/folders",
                auth=self._auth
            )
        elif folder:
            response =  browser.get(
                    self._api_url + "folders/" + folder.Folder_id + "/folders",
                    auth=self._auth
                    )
        else:
            raise ValueError("No argument for get_folders provided, need Course or Folder")
        
        folders_list = []
        for f in response.get("data", {}):
            folder = Folder (
                    Folder_id=f["id"],
                    Name=safe_get(f, "attributes", "name"),
                    Description=safe_get(f, "attributes", "description"),
                    Creation_Date=safe_get(f, "attributes", "mkdate"),
                    Change_Date=safe_get(f, "attributes", "chdate"),
                    )
            folders_list.append(folder)
        return folders_list
    
    def get_files(self, course: Optional[Course] = None, folder: Optional[Folder] = None) -> list[File]:
        if course:
            resp = browser.get(
                    self._api_url + "courses/" + course.Course_id + "/file-refs",
                    auth=self._auth
                    )
        elif folder:
            resp = browser.get(
                    self._api_url + "folders/" + folder.Folder_id + "/file-refs",
                    auth=self._auth
                    )
        else:
            raise ValueError("No argument for get_files provided, need Course or Folder")
       
        files_list = []
        for f in resp.get("data", {}):
            file = File(
                    File_id = f["id"],
                    Name = safe_get(f, "attributes", "name"),
                    Description = safe_get(f, "attributes", "description"),
                    Creation_Date = safe_get(f, "attributes", "mkdate"),
                    Change_Date = safe_get(f, "attributes", "chdate"),
                    Owner_Name = safe_get(f, "relationships", "owner", "meta", "name"),
                    Owner_id = safe_get(f, "relationships", "owner", "data", "id")
                    )
            files_list.append(file)
        return files_list

    def download_file(self, file: File) -> bytes:
        """returns bytes of file content, needs specific file id"""
        return browser.download(
                self._api_url + "file-refs/" + File.File_id + "/content", auth=self._auth
                )

    def change_metadata(self, metadata: File_Metadata, file: Optional[File] = None, file_id = None):
        if file:
            file_id = File.File_id

        headers = {
                'Content-Type': 'application/vnd.api+json',
                }

        payload = {
                "data": {
                    "type": "file-refs",
                    "id": file_id,
                    "attributes": {
                        "name": metadata.Name,
                        "description": metadata.Description
                        },
                    'relationships': {
                        'terms-of-use': {
                            'data': {
                                'type': 'terms-of-use',
                                'id': metadata.License
                                }
                            }
                        }}}

        response = browser.patch(
                url = self._api_url + "file-refs/" + file_id,
                headers = headers,
                auth = self._auth,
                json = payload
                )

        return response

    def upload_file(self, folder: Folder, file_binary: bytes, metadata: Optional[File_Metadata] = None):
        """uploads file with metadato to folder"""

        file_dict = {'file': file_binary}

        response = browser.upload(
                url = self._api_url + "folders/" + folder.Folder_id + "/file-refs",
                content_dict = file_dict,
                auth = self._auth,
                expected_status_code = 201
                )

        file_id = response.headers.get("Location").split("/")[-1]

        if metadata:
            # change metadata of file in second step
            response = self.change_metadata(metadata=metadata, file_id=file_id)
            return response

        else:
            return response

