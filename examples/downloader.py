import os
import studipy
from dotenv import load_dotenv


# define which output folders should be used and what folders on studip will be used to download its files and put them all into the defined folder
config = {
    "computer-science": ["computer science id", "computer science id 2"],
}

load_dotenv()

# get username and password from environment

username = os.getenv("STUDIP_LOGINNAME")
password = os.getenv("STUDIP_LOGINSECRET")
base_url = os.getenv("STUDIP_BASEURL")

# set a base folder where all the predifined subfolders will be

base_folder = "<output folder>"


# create the studipy Client object

client = studipy.Client(username=username, password=password, base_url=base_url)

def download_folder(folder_id, output_folder_name, folder):
    output_folder = os.path.join(base_folder, output_folder_name)
    folder_data = client.get_folder_files(folder_id)["data"]
    files = {}
    for file in folder_data:
        file_name = file["attributes"]["name"]
        files[file_name] = file["id"]

    existing_files = [f for f in os.listdir(output_folder) if os.path.isfile(os.path.join(output_folder, f))]

    for file in files.keys():
        if file not in existing_files:
            with open(os.path.join(output_folder, file), "wb") as fw:
                fw.write(client.download_file(files[file]))
        else:
            print("skipping ", file)

# go though config and download folder contents

for lecture in config.keys():
    for id in config[lecture]:
        download_folder(output_folder_name=lecture, folder_id=id)
