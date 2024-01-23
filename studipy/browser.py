import requests
import json

class StudipError(Exception):
    pass

def get(url, auth, params={}) -> object:
    response = requests.get(url, auth=auth, params=params)
    check_status(status_code=response.status_code, url=url)
    return json.loads(response.text)

def download(url, auth) -> bytes:
    response = requests.get(url, auth=auth, stream=True)
    check_status(status_code=response.status_code, url=url)
    return response.content

def check_status(status_code, url):
    match status_code:
        case 401:
            raise StudipError(f"Unauthorized! tried accessing {url} with status code {status_code}")
        case 403:
            raise StudipError(f"Forbidden! tried accessing {url} with status code {status_code}")
        case 404:
            raise StudipError(f"Not Found! tried accessing {url} with status code {status_code}")