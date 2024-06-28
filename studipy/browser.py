import requests
import json

def get(url, auth, params=None, expected_status_code=200) -> object:
    """Returns JSON response from API."""
    response = requests.get(
        url=url,
        auth=auth,
        params=params
    )
    check_status(
        status_code=response.status_code,
        url=url,
        expected=expected_status_code
    )
    return json.loads(response.text)

def patch(url, auth, params=None, json=None, data=None, headers=None, expected_status_code=200):
    """Patches over API."""
    response = requests.patch(
        url=url,
        auth=auth,
        params=params,
        data=data,
        headers=headers,
        json=json
    )
    check_status(
        status_code=response.status_code,
        url=url,
        expected=expected_status_code
    )
    return response

def download(url, auth, expected_status_code=200) -> bytes:
    """Returns binary response from API."""
    response = requests.get(
        url=url,
        auth=auth,
        stream=True
    )
    check_status(
        status_code=response.status_code,
        url=url,
        expected=expected_status_code
    )
    return response.content

def upload(url, content_dict: dict, auth, expected_status_code=200):
    """Uploads file to URL."""
    response = requests.post(
        url=url,
        auth=auth,
        files=content_dict
    )
    check_status(
        status_code=response.status_code,
        url=url,
        expected=expected_status_code
    )
    return response

def check_status(status_code, expected, url):
    """raises error based on status code"""
    match status_code:
        case 400:
            raise requests.HTTPError(f"Faulty Request! tried accessing {url} with status code {status_code}")
        case 401:
            raise requests.HTTPError(f"Unauthorized! tried accessing {url} with status code {status_code}")
        case 403:
            raise requests.HTTPError(f"Forbidden! tried accessing {url} with status code {status_code}")
        case 404:
            raise requests.HTTPError(f"Not Found! tried accessing {url} with status code {status_code}")
        case _ if expected != status_code:
            raise requests.HTTPError(f"Unexpected Status Code {status_code}, expected {expected} on URL {url}")
