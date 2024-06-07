import requests
import json

class StudipError(Exception):
    """default Exception if Studip Request fails"""
    pass

def get(url, auth, params=None) -> object:
    """returns json response from api"""
    response = requests.get(url, auth=auth, params=params)
    check_status(status_code=response.status_code, url=url)
    return json.loads(response.text)

def download(url, auth) -> bytes:
    """returns binary response from api"""
    response = requests.get(url, auth=auth, stream=True)
    check_status(status_code=response.status_code, url=url)
    return response.content

def check_status(status_code, url):
    """raises error based on status code"""
    match status_code:
        case 401:
            raise StudipError(f"Unauthorized! tried accessing {url} with status code {status_code}")
        case 403:
            raise StudipError(f"Forbidden! tried accessing {url} with status code {status_code}")
        case 404:
            raise StudipError(f"Not Found! tried accessing {url} with status code {status_code}")

