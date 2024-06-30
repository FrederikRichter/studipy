import studipy
from studipy.types import File_Metadata, Message
import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("STUDIP_LOGINNAME")
password = os.getenv("STUDIP_LOGINSECRET")
base_url = os.getenv("STUDIP_BASEURL")

# create a new client object
client = studipy.Client(username=username, password=password, base_url=base_url)



def run_tests():
    LICENSES = client.Constants.LICENSES
    LICENSES[0].license_id
    print("constants tests passed")

    courses = client.Courses.get_courses()
    courses[0].course_id
    print("courses test passed")
    
    messages = client.Messages.get_messages()
    messages[0].message_id
    _test_message = Message (
                subject="test subject",
                body="test body",
                creation_date=None,
                sender_id=None,
                message_id=None
            )
    _resp = client.Messages.send_message(message=_test_message, recipient_ids=[client.me.user_id])
    _test_message_id = _resp.json()["data"]["id"] 
    client.Messages.delete_message(message_id=_test_message_id)
    print("messages test passed")

    users = client.Users.get_users(limit=20)
    users[0].user_id
    print("users test passed")

    folders = client.Files.get_folders(course=courses[0])
    folders[0].folder_id
    sub_folders = client.Files.get_folders(folder=folders[0])
    sub_folders[0].folder_id
    files = client.Files.get_files(folder=sub_folders[0])
    
    client.Files.read_file(file=files[0])
    client.Files.download_file(file=files[0])
    
    _private_folder = "0d3f60fa710b7b9d23638b46b83de307"
    _test_file = open("testing.py", "rb")
    _test_license = LICENSES[0]
    _test_Metadata = File_Metadata(
                name="Testing",
                license=_test_license,
                description="Test description"
            )
    _test_file_id = client.Files.upload_file(folder_id=_private_folder, file_binary=_test_file)
    client.Files.delete_file(file_id=_test_file_id)
    print("files test passed")

run_tests()
