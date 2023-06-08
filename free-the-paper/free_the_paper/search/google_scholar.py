from dataclasses import dataclass

from bs4 import BeautifulSoup, Tag
from requests import Response
from requests.exceptions import RequestException

from ..exceptions import CaptchaError, PapersNotFoundError
from .. import session


__all__ = ['GoogleScholar']


@dataclass
class ScholarPaper:

    def __init__(self, tag: Tag) -> None:
        self.tag: Tag = tag

    def name(self) -> str:
        return self._link_tag().text

    def source(self) -> str | None:
        if self._pdf_tag():
            return self._pdf_tag().find('a')['href']
        if self._link_tag().find('a'):
            return self._link_tag().find('a')['href']

    def has_table(self) -> bool:
        return bool(self.tag.find('table'))

    def _link_tag(self) -> Tag:
        return self.tag.find('h3', class_='gs_rt')

    def _pdf_tag(self) -> Tag | None:
        return self.tag.find('div', class_='gs_ggs gs_fl')


class GoogleScholar:

    SCHOLAR_BASE_URL = 'https://scholar.google.com/scholar'

    def __init__(self):
        self.session = session.get_session()

    def search(self, query: str, limit: int = 10) -> list[tuple[str, str]]:
        start_index = 0
        results = []
        while len(results) < limit:
            try:
                papers = self._page_search(query, start_index)
            except (RequestException, CaptchaError, PapersNotFoundError):
                return results
            else:
                results += papers[:limit - len(results)]
                start_index += 10
        return results

    def _get_response(self, query: str, start_index: int = 0) -> Response:
        try:
            response = self.session.get(self.SCHOLAR_BASE_URL, params={'q': query, 'start': start_index})
        except RequestException:
            raise
        if 'CAPTCHA' in str(response.content):
            raise CaptchaError
        return response

    def _page_search(self, query: str, start_index: int) -> list[tuple[str, str]]:
        soup = session.make_soup(self._get_response(query, start_index))
        papers = self._extract_papers(soup)
        return [(paper.name, paper.source) for paper in papers if (not paper.has_table and paper.source)]

    @staticmethod
    def _extract_papers(soup: BeautifulSoup) -> list[ScholarPaper]:
        papers = [ScholarPaper(tag) for tag in soup.find_all('div', class_="gs_r")]
        if len(papers) == 0:
            raise PapersNotFoundError
        return papers
