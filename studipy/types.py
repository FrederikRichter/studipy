from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    Name: str
    Username: str
    E_Mail: Optional[str]
    User_id: str

class Course(BaseModel):
    Title: str
    Subtitle: Optional[str]
    Description: Optional[str]
    Location: Optional[str]
    Course_id: str

class Message(BaseModel):
    Title: str
    Message_id: str
    Sender_id: Optional[str]
    Body: Optional[str]
    Creation_Date: str

class File(BaseModel):
    Name: str
    File_id: str
    Timestamp: int
    Creator: User

class Folder(BaseModel):
    Name: str
    Folder_id: str
    Timestamp: int
    Creator: str
    File_List: list[File]
