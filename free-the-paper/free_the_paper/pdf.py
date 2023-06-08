import requests
from requests import Response

from .exceptions import NoUrlAvailableError, ResponseContentError
from . import session


def is_direct_url(url: str) -> bool:
    return url.startswith('http') and url.endswith('.pdf')


def fetch_url(url: str) -> Response:
    try:
        return session.get_response(url, verify=False)
    except (requests.exceptions.ConnectionError, requests.exceptions.RequestException) as err:
        raise NoUrlAvailableError from err


def read_response(response: Response) -> bytes:
    if response.headers['Content-Type'] == 'application/pdf':
        return response.content
    raise ResponseContentError()


def save(pdf: bytes, path: str) -> None:
    with open(path, 'wb') as file:
        file.write(pdf)
