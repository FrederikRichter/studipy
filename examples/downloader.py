import os
import studipy
from studipy.types import File
from dotenv import load_dotenv

config = {
    "agla-II-Skripte": ["a261cf018699ff97b9fcf3df50d1ca18"],
    "agla-II-Zettel": ["c4c7cd29e204f46823b8873dae21a993"],
    "diff-II-Skripte": [],
    "diff-II-Zettel": ["fe9c696556ab6e89fab70fa5b62fb936"],
    "diff-II-Bonus-Zettel": [],
}

load_dotenv()

username = os.getenv("STUDIP_LOGINNAME")
password = os.getenv("STUDIP_LOGINSECRET")
base_url = os.getenv("STUDIP_BASEURL")

base_folder = "/home/frederik/Scripts/studip/zettel"

client = studipy.Client(username=username, password=password, base_url=base_url)

def download_folder(folder_id, output_folder_name):
    output_folder = os.path.join(base_folder, output_folder_name)
    files: list[File] = client.Files.get_files(folder_id=folder_id)
    
    try:
        existing_files = [f for f in os.listdir(output_folder) if os.path.isfile(os.path.join(output_folder, f))]
    except FileNotFoundError:
        os.mkdir(output_folder)
        existing_files = [f for f in os.listdir(output_folder) if os.path.isfile(os.path.join(output_folder, f))]

    for f in files:
        if f.name not in existing_files:
            print("downloading", f.name)
            try:
                with open(os.path.join(output_folder, f.name), "wb") as fw:
                    fw.write(client.Files.download_file(file_id=f.file_id))
            except AttributeError:
                print("skipping")
        else:
            print("skipping ", f)

for lecture in config.keys():
    for id in config[lecture]:
        download_folder(output_folder_name=lecture, folder_id=id)
