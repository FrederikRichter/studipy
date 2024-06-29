from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    Name: Optional[str]
    Username: Optional[str]
    E_Mail: Optional[str]
    User_id: str

class Course(BaseModel):
    Title: Optional[str]
    Subtitle: Optional[str]
    Description: Optional[str]
    Location: Optional[str]
    Course_id: str

class Message(BaseModel):
    Title: str
    Message_id: Optional[str]
    Sender_id: Optional[str]
    Body: Optional[str]
    Creation_Date: Optional[str]

class License(BaseModel):
    License_id: str
    Name: Optional[str]
    Description: Optional[str]

class File(BaseModel):
    Name: Optional[str]
    File_id: str
    Creation_Date: Optional[str]
    Change_Date: Optional[str]
    Description: Optional[str]
    Owner_Name: Optional[str]
    Owner_id: Optional[str]

class File_Metadata(BaseModel):
    Name: Optional[str]
    Description: Optional[str]
    License: License

class Folder(BaseModel):
    Name: Optional[str]
    Folder_id: str
    Creation_Date: Optional[str]
    Change_Date: Optional[str]
    Description: Optional[str]
