[![PyPI Downloads](https://img.shields.io/pypi/dm/studipy.svg?label=PyPI%20downloads)](
https://pypi.org/project/studipy/) [(https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white)]

# studipy - StudIP python API
StudIP Python API wrapper using StudIPs JSONAPI

Easy to use and strongly typed

# INSTALLATION
```
pip install --upgrade studipy
```

## From source
```
poetry build
pip install dist/....
```

# Usage - Example
```python
import studipy
import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("STUDIP_LOGINNAME")
password = os.getenv("STUDIP_LOGINSECRET")
base_url = os.getenv("STUDIP_BASEURL")

# create a new client object
client = studipy.Client(username=username, password=password, base_url=base_url)

# get a list of Course objects (specified in types.py)
courses = client.Courses.get_courses()
for c in courses:
        print(c.title)
```

# Roadmap

## Authentication
- [x] Basic (Username, Password)
- [ ] Oauth

## Users
- [x] Get Users
- [x] Get Self
- [x] Search for Users

## Messages
- [x] Get Messages
- [x] Send Messages
- [x] Delete Messages
- [x] Mark Messages Read/Unread

## Files and Folders
- [x] Get Course Folders
- [x] Get Subfolders
- [x] Get Files in Folder
- [x] Upload Files
- [x] Delete Files
- [x] Change File Metadata
- [ ] Change File Content
- [x] Download Files
- [x] Mark files read
- [ ] Move Folders/Files
- [ ] Copy Folders/Files

## Calendar
- [ ] View Calendar
- [ ] Download Calendar ics (rewrite)
- [ ] Edit Calendar

## Plugins
You will have to implement custom plugins yourself. They might have registered JSONAPI notes, good luck

## Documentation
- [ ] Write Documentation
- [ ] Extend Examples

<table>
  <tr>
    <td><a href="https://www.paypal.me/FrederikRichter/"><img width="256" src="coffee.png" /><p align="center">Buy me a Coffee!</p></a></td>
  </tr>
</table>
