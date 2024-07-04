import studipy
from studipy.types import Metadata, Message
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Get the necessary credentials and base URL from environment variables
username = os.getenv("STUDIP_LOGINNAME")
password = os.getenv("STUDIP_LOGINSECRET")
base_url = os.getenv("STUDIP_BASEURL")

# Create a new client object for interacting with the Stud.IP API
client = studipy.Client(username=username, password=password, base_url=base_url)

def run_tests():
    # Test for retrieving licenses and accessing their IDs
    LICENSES = client.Constants.LICENSES
    LICENSES[0].license_id
    print("constants tests passed")

    # Test for retrieving courses and accessing their IDs
    courses = client.Courses.get_courses()
    courses[0].course_id
    print("courses test passed")
    
    # Test for retrieving messages, viewing a message, sending, and deleting a message
    messages = client.Messages.get_messages()
    assert messages[0] == client.Messages.view_message(message=messages[0])
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

    # Test for retrieving users, accessing their IDs, and searching users
    users = client.Users.get_users(limit=20)
    users[0].user_id
    client.Users.get_users(search_q="test") 
    print("users test passed")

    # Test for retrieving folders and subfolders
    folders = client.Files.get_folders(course=courses[0])
    folders[0].folder_id
    sub_folders = client.Files.get_folders(folder=folders[0])
    sub_folders[0].folder_id
    
    # Test for retrieving files and reading/downloading them
    files = client.Files.get_files(folder=sub_folders[0])    
    client.Files.read_file(file=files[0])
    client.Files.download_file(file=files[0])
    
    # Test for uploading file, changing metadata and deleting it
    _private_folder = "0d3f60fa710b7b9d23638b46b83de307"
    _test_file = open("testing.py", "rb")
    _test_license = LICENSES[0]
    _test_metadata = Metadata(
                name="Testing",
                license=_test_license,
                description="Test description"
            )
    _test_file_id = client.Files.upload_file(folder_id=_private_folder, file_binary=_test_file)
    _test_update_file = open("coffee.png", "rb")
    client.Files.change_file_content(file_id=_test_file_id, file_binary=_test_update_file)
    client.Files.change_metadata(file_id=_test_file_id, metadata=_test_metadata)
    client.Files.delete_file(file_id=_test_file_id)

    # Test for creating 2 Folders, moving one into another and deleting everything
    _root_metadata = Metadata(
            name="Testing root",
            license=_test_license,
            description="Test description"
            )
    _root_id = client.Files.create_folder(location_id=_private_folder, metadata=_root_metadata)
    _to_move_metadata = Metadata(
            name="Testing to move",
            license=_test_license,
            description="Test description"
            )
    _move_id = client.Files.create_folder(location_id=_private_folder, metadata=_to_move_metadata)
    client.Files.move_folder(folder_id=_move_id, target_folder_id=_root_id)

    # cleanup
    client.Files.delete_folder(folder_id=_root_id)
    print("files test passed")

# Run all tests
run_tests()
