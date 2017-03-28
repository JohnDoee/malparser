import urllib2

from malparser.anime import Anime
from malparser.manga import Manga

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en",
    "User-Agent": "Scrapy/0.24.2 (+http://scrapy.org)",
}

class MAL(object):
    def _fetch(self, obj):
        req = urllib2.Request(obj._get_url(), None, HEADERS)
        data = urllib2.urlopen(req).read()
        obj.parse(data)
    
    def _handle_related(self, obj):
        related = {'manga': Manga, 'anime': Anime}
        
        for key, values in obj.related.items():
            obj.related[key] = [related[v['type']](v['id'], self) for v in values]
    
    def get_anime(self, mal_id):
        return Anime(mal_id, self)
    
    def get_manga(self, mal_id):
        return Manga(mal_id, self)
