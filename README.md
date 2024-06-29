[![PyPI Downloads](https://img.shields.io/pypi/dm/studipy.svg?label=PyPI%20downloads)](
https://pypi.org/project/studipy/)

# studipy
StudIP Python API library using JSONAPI

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

client = studipy.Client(username=username, password=password, base_url=base_url)

courses = client.Courses.get_courses()
for c in courses:
        print(c.Title)
```

# Checklist
- [x] Auth
- [x] Get Users
- [x] Get Messages
- [x] Send Messages
- [x] Get Course Folders
- [x] Get Subfolders
- [x] Get Files in Folder
- [x] Upload Files
- [x] Delete Files
- [x] Change File Metadata
- [x] Download Files
- [x] Mark files read
- [ ] Delete Messages
- [ ] Plugin Support
- [ ] Mark Messages Read/Unread
- [ ] View Calendar
- [ ] Download Calendar ics (rewrite)
- [ ] Edit Calendar

<table>
  <tr>
    <td><a href="https://www.paypal.me/FrederikRichter/"><img width="256" src="coffee.png" /><p align="center">Buy me a Coffee!</p></a></td>
  </tr>
</table>
