import requests

from .anime import Anime
from .manga import Manga
from .searchresult import SearchResult

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en",
    "User-Agent": "Scrapy/0.24.2 (+http://scrapy.org)",
}


class FailedToFetchException(Exception):
    pass


class MAL(object):
    def _fetch(self, obj):
        for i in range(2, 4):
            r = requests.get(obj._get_url(), headers=HEADERS)
            if r.status_code != 200:
                time.sleep(i)
            else:
                break
        else:
            raise FailedToFetchException('Tried 3 times and was unable to fetch page')

        data = r.text
        obj.parse(data)
        obj.fetched = True

    def _handle_related(self, obj):
        related = {'manga': Manga, 'anime': Anime}

        for key, values in obj.related.items():
            obj.related[key] = [related[v['type']](v['id'], self) for v in values]

    def get_anime(self, mal_id):
        return Anime(mal_id, self)

    def get_manga(self, mal_id):
        return Manga(mal_id, self)

    def search_anime(self, query):
        return SearchResult('anime', query, self)
