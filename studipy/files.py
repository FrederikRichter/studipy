import studipy.browser as browser
from studipy.types import Folder, File, Course, Metadata
from studipy.helper import safe_get
from typing import Optional
import requests

class Files:
    def __init__(self, client):
        self._client = client
        self._auth = client._auth
        self._api_url = client._api_url
        self._me = client.me

    def get_folders(self, course: Optional[Course] = None, folder: Optional[Folder] = None, folder_id: Optional[str] = None) -> list[Folder]:
        """returns list of Folders in a course"""
        if folder:
            folder_id = folder.folder_id
        if course:
            course_id = course.course_id

        if "course_id" in locals():
            response = browser.get(
                self._api_url + "courses/" + course_id + "/folders",
                auth=self._auth
            )
        elif "folder_id" in locals():
            response =  browser.get(
                    self._api_url + "folders/" + folder_id + "/folders",
                    auth=self._auth
                    )
        else:
            raise ValueError("No argument for get_folders provided, need Course or Folder")
        
        folders_list = []
        for f in response.get("data", {}):
            folder = Folder (
                    folder_id=f["id"],
                    name=safe_get(f, "attributes", "name"),
                    description=safe_get(f, "attributes", "description"),
                    creation_date=safe_get(f, "attributes", "mkdate"),
                    change_date=safe_get(f, "attributes", "chdate"),
                    )
            folders_list.append(folder)
        return folders_list
    
    def get_files(self, course: Optional[Course] = None, folder: Optional[Folder] = None, folder_id: Optional[str] = None, course_id: Optional[str] = None) -> list[File]:
        if course or course_id:
            if course:
                course_id = course.course_id
            resp = browser.get(
                    self._api_url + "courses/" + course_id + "/file-refs",
                    auth=self._auth
                    )
        elif folder or folder_id:
            if folder:
                folder_id = folder.folder_id
            resp = browser.get(
                    self._api_url + "folders/" + folder_id + "/file-refs",
                    auth=self._auth
                    )
        else:
            raise ValueError("No argument for get_files provided, need Course or Folder")
       
        files_list = []
        for f in resp.get("data", {}):
            file = File(
                    file_id = f["id"],
                    name = safe_get(f, "attributes", "name"),
                    description = safe_get(f, "attributes", "description"),
                    creation_date = safe_get(f, "attributes", "mkdate"),
                    change_date = safe_get(f, "attributes", "chdate"),
                    owner_name = safe_get(f, "relationships", "owner", "meta", "name"),
                    owner_id = safe_get(f, "relationships", "owner", "data", "id")
                    )
            files_list.append(file)
        return files_list

    def download_file(self, file: Optional[File] = None, file_id = None) -> bytes:
        """returns bytes of file content, needs specific file id"""
        if file:
            file_id = file.file_id

        return browser.download(
                url = self._api_url + "file-refs/" + file_id + "/content", auth=self._auth
                )

    
    def read_file(self, file: Optional[File] = None, file_id = None) -> dict:
        """returns bytes of file content, needs specific file id"""
        if file:
            file_id = file.file_id

        response = browser.get(
                url=self._api_url + "file-refs/" + file_id, auth=self._auth
                )
        return response
        
    def delete_file(self, file: Optional[File] = None, file_id = None, expected_status_code=204) -> requests.Response:
        """returns bytes of file content, needs specific file id"""
        if file:
            file_id = file.file_id

        response = browser.delete(
                url=self._api_url + "file-refs/" + file_id, auth=self._auth, expected_status_code=expected_status_code
                )
        return response
    
    
    def delete_folder(self, folder: Optional[Folder] = None, folder_id = None, expected_status_code=204) -> requests.Response:
        """returns bytes of file content, needs specific file id"""
        if folder:
            folder_id = folder.folder_id

        response = browser.delete(
                url=self._api_url + "folders/" + folder_id, auth=self._auth, expected_status_code=expected_status_code
                )
        return response

    def change_metadata(self, metadata: Metadata, file: Optional[File] = None, file_id: Optional[str] = None, folder: Optional[Folder] =None, folder_id: Optional[str] = None):
        if file:
            file_id = file.file_id
        
        if folder:
            folder_id = folder.folder_id

        if file_id:
            payload = {
                    "data": {
                        "type": "file-refs",
                        "id": file_id,
                        "attributes": {
                            "name": metadata.name,
                            "description": metadata.description
                            },
                        'relationships': {
                            'terms-of-use': {
                                'data': {
                                    'type': 'terms-of-use',
                                    'id': metadata.license.license_id
                                    }
                                }
                            }}}

            response = browser.patch(
                    url = self._api_url + "file-refs/" + file_id,
                    auth = self._auth,
                    json = payload
                    )
        elif folder_id:
            payload = {
                    "data": {
                        "type": "folders",
                        "id": folder_id,
                        "attributes": {
                            "name": metadata.name,
                            "description": metadata.description
                            },
                        'relationships': {
                            'terms-of-use': {
                                'data': {
                                    'type': 'terms-of-use',
                                    'id': metadata.license.license_id
                                    }
                                }
                            }}}

            response = browser.patch(
                    url = self._api_url + "folders/" + folder_id,
                    auth = self._auth,
                    json = payload
                    )
        else:
            raise KeyError("neither folder/id nor file/id for change metadata provided")

        return response


    def change_file_content(self,  file_binary: bytes, file: Optional[File] = None, file_id: Optional[str] = None) -> requests.Response:
        """uploads file with metadata to folder"""
        
        if file:
            file_id = file.file_id

        file_dict = {'file': file_binary}

        response = browser.upload(
                url = self._api_url + "file-refs/" + file_id + "/content",
                content_dict = file_dict,
                auth = self._auth,
                expected_status_code = 201
                )

        return response


    def upload_file(self,  file_binary: bytes, folder: Optional[Folder] = None, folder_id: Optional[str] = None, metadata: Optional[Metadata] = None) -> str:
        """uploads file with metadata to folder"""
        
        if folder:
            folder_id = folder.folder_id

        file_dict = {'file': file_binary}

        response = browser.upload(
                url = self._api_url + "folders/" + folder_id + "/file-refs",
                content_dict = file_dict,
                auth = self._auth,
                expected_status_code = 201
                )

        file_id = response.headers["Location"].split("/")[-1]

        if metadata:
            # change metadata of file in second step
            response = self.change_metadata(metadata=metadata, file_id=file_id)
            return file_id

        else:
            return file_id

    def create_folder(self,  location: Optional[Folder] = None, location_id: Optional[str] = None, metadata: Optional[Metadata] = None):
        if location:
            location_id = location.folder_id
        
        payload = {
                "data": {
                    "type": "folders",
                    "attributes": {
                        "name":"New Folder"
                        }
                    }
                }
        response = browser.post(
                url = self._api_url + "folders/" + location_id + "/folders",
                auth = self._auth,
                json = payload,
                expected_status_code = 201
                )

        folder_id = response.headers["Location"].split("/")[-1]
        if metadata:
            # change metadata of file in second step
            response = self.change_metadata(metadata=metadata, folder_id=folder_id)
            return folder_id
        else:
            return folder_id


    def move(self, folder: Optional[Folder] = None, folder_id: Optional[str] = None, file: Optional[File] = None, file_id: Optional[str] = None, target_folder: Optional[Folder] = None, target_folder_id: Optional[str] = None) -> requests.Response:
        if folder:
            folder_id = folder.folder_id
        if file:
            file_id = file.file_id
        if target_folder:
            target_folder_id = target_folder.folder_id
        
        if folder_id:
            payload = {
                    "data": {
                        "type": "folders",
                        "id": folder_id,
                        "relationships": {
                            "parent" :{
                                "links":
                                {
                                    "related" : "/jsonapi.php/v1/folders/" + str(target_folder_id)
                                    },
                                "data":
                                {
                                    "type": "folders",
                                    "id" : str(target_folder_id)
                                    }
                                }
                            }
                        }
                    }
            response = browser.patch(
                    url = self._api_url + "folders/" + folder_id,
                    auth = self._auth,
                    json = payload
                    )
        elif file_id:
            try:
                payload = {
                        "data": {
                            "type": "file-refs",
                            "id": file_id,
                            "relationships": {
                                "parent" :{
                                    "links":
                                    {
                                        "related" : "/jsonapi.php/v1/folders/" + str(target_folder_id)
                                        },
                                    "data":
                                    {
                                        "type": "folders",
                                        "id" : str(target_folder_id)
                                        }
                                    }
                                }
                            }
                        }
                response = browser.patch(
                        url = self._api_url + "file-refs/" + file_id,
                        auth = self._auth,
                        json = payload
                        )
            except requests.HTTPError:
                raise NotImplementedError("""
                                          Even though this should work,
                                          it is not yet implemented by studip.
                                          Please only move folders.
                                          To workaround copy file and delete original
                                          ~Frederik"""
                                          )
        else:
            raise KeyError("Neither file/id nor folder/id provided for move file/folder")
        return response

    def copy(self, folder: Optional[Folder] = None, folder_id: Optional[str] = None, file: Optional[File] = None, file_id: Optional[str] = None, target_folder: Optional[Folder] = None, target_folder_id: Optional[str] = None) -> requests.Response:
        raise NotImplementedError("""
        Since my university does not have the newest
        studip version i cannot test this. Might fix this once i get proper
        access to a testing environment
        """)
        if folder:
            folder_id = folder.folder_id
        if file:
            file_id = file.file_id
        if target_folder:
            target_folder_id = target_folder.folder_id

        if folder_id:
            file_dict = {'destination': target_folder_id}

            response = browser.post(
                    url = self._api_url + "folders/" + folder_id + "/copy",
                    files = file_dict,
                    auth = self._auth,
                    expected_status_code = 201
                    )
