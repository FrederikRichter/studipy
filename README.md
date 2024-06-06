[![PyPI Downloads](https://img.shields.io/pypi/dm/studipy.svg?label=PyPI%20downloads)](
https://pypi.org/project/studipy/)

# studipy
StudIP Python API library using JSONAPI

# INSTALLATION
```
pip install studipy
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

client.get_courses()
```

<table>
  <tr>
    <td><a href="https://www.paypal.me/FrederikRichter/"><img width="256" src="coffee.png" /><p align="center">Buy me a Coffee!</p></a></td>
  </tr>
</table>
