import json
import sys

from requests.compat import quote_plus

from .base import Base
from .anime import Anime


class SearchResult(Base):
    base_url = 'https://myanimelist.net/search/prefix.json?type=%s&keyword=%s&v=1'

    def __init__(self, search_type, query, mal):  # search_type: anime, manga
        self.search_type = search_type
        if sys.version_info[0] < 3 and isinstance(query, unicode):
            query = query.encode('utf-8')
        self.mal_id = quote_plus(query)
        self.mal = mal

    def _get_url(self):
        return self.base_url % (self.search_type, self.mal_id, )

    def parse(self, html):
        self.results = []
        results = json.loads(html)['categories'][0]['items']
        for result in results:
            if result['type'] == 'anime':
                item = Anime(result['id'], self.mal)
                item.reset()
                item.title = result['name']

                cover_url = result['image_url'].split('?')[0].split('/')
                del cover_url[3]
                del cover_url[3]
                item.cover = '/'.join(cover_url)

                payload = result['payload']
                if 'aired' in payload:
                    item.aired['Aired_start'], item.aired['Aired_end'], item.aired['Season'] = self.convert_aired_dates(payload['aired'])
                    item.info['Aired'] = payload['aired']

                item.info['Status'] = payload['status']
                item.info['Type'] = payload['media_type']
                item.statistics['Score'] = payload['score']

                self.results.append(item)
