import studipy
from studipy.types import File_Metadata
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
    print("constants tests passed")

    courses = client.Courses.get_courses()
    print("courses test passed")
    
    client.Messages.get_messages()
    print("messages test passed")

    users = client.Users.get_users(limit=20)
    print("users test passed")

    folders = client.Files.get_folders(course=courses[0])
    sub_folders = client.Files.get_folders(folder=folders[0])
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
