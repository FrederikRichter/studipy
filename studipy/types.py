from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    name: Optional[str]
    username: Optional[str]
    email: Optional[str]
    user_id: str

class Course(BaseModel):
    title: Optional[str]
    subtitle: Optional[str]
    description: Optional[str]
    location: Optional[str]
    course_id: str

class Message(BaseModel):
    subject: str
    message_id: Optional[str]
    sender_id: Optional[str]
    body: Optional[str]
    creation_date: Optional[str]

class License(BaseModel):
    license_id: str
    name: Optional[str]
    description: Optional[str]

class File(BaseModel):
    name: Optional[str]
    file_id: str
    creation_date: Optional[str]
    change_date: Optional[str]
    description: Optional[str]
    owner_name: Optional[str]
    owner_id: Optional[str]

class File_Metadata(BaseModel):
    name: Optional[str]
    description: Optional[str]
    license: License

class Folder(BaseModel):
    name: Optional[str]
    folder_id: str
    creation_date: Optional[str]
    change_date: Optional[str]
    description: Optional[str]
