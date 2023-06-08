from bs4 import BeautifulSoup
import requests

from ..exceptions import DirectUrlNotFoundError
from .. import session


__all__ = ['SciHub']


class SciHubBaseUrls:

    URL = 'https://sci-hub.now.sh/'

    def get_urls_list(self) -> list[str]:
        return [a['href'] for a in self._homepage_a_tags() if 'sci-hub.' in a['href']]

    def _homepage_soup(self) -> BeautifulSoup:
        response = requests.get(self.URL)
        return session.make_soup(response)

    def _homepage_a_tags(self) -> list:
        return self._homepage_soup().find_all('a', href=True)


class SciHub:

    def __init__(self) -> None:
        self._base_urls = SciHubBaseUrls().get_urls_list()

    def search_url(self, paper_id: str) -> str:
        for base_url in self._base_urls:
            url = self._get_direct_url(paper_id, base_url)
            if url is not None:
                return url
        raise DirectUrlNotFoundError()

    @staticmethod
    def _get_direct_url(base_url: str, paper_id: str) -> str | None:
        iframe = session.get_soup(base_url + paper_id, verify=False).find('iframe')
        if iframe:
            src = iframe.get('src')
            return ('http:' + src) if src.startswith('//') else src
        return None
