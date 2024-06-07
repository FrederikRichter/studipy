import requests
import json
from typing import Any, Dict, Optional

class StudipError(Exception):
    """default Exception if Studip Request fails"""
    pass

def get(url: str, auth: tuple[str, str], params: Optional[Dict[str, Any]] = None) -> Any:
    """returns json response from api"""
    response = requests.get(url, auth=auth, params=params)
    check_status(status_code=response.status_code, url=url)
    return json.loads(response.text)

def download(url: str, auth: tuple[str, str]) -> bytes:
    """returns binary response from api"""
    response = requests.get(url, auth=auth, stream=True)
    check_status(status_code=response.status_code, url=url)
    return response.content

def check_status(status_code: int, url: str) -> None:
    """raises error based on status code"""
    match status_code:
        case 401:
            raise StudipError(f"Unauthorized! tried accessing {url} with status code {status_code}")
        case 403:
            raise StudipError(f"Forbidden! tried accessing {url} with status code {status_code}")
        case 404:
            raise StudipError(f"Not Found! tried accessing {url} with status code {status_code}")
