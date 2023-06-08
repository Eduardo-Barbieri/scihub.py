from bs4 import BeautifulSoup
from requests import Response, Session


SESSION_HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0'}


def get_session(proxy: str | None = None) -> Session:
    session = Session()
    session.headers = SESSION_HEADERS
    if proxy is not None:
        session.proxies = {'http': proxy, 'https': proxy}
    return session


def get_response(url: str, proxy: str | None = None, **kwargs) -> Response:
    return get_session(proxy).get(url, **kwargs)


def make_soup(response: Response) -> BeautifulSoup:
    return BeautifulSoup(response.content, 'html.parser')


def get_soup(url: str, proxy: str | None = None, **kwargs) -> BeautifulSoup:
    return make_soup(get_response(url, proxy, **kwargs))