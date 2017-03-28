MAL Parser
=====================

Library to parse [MyAnimeList] pages, contains lots more features than un-official API

Getting started
---------------

To get it up and running, do::

```sh
pip install malparser
```

This is an example of almost anything this library can:
```python
>>> from malparser import MAL
>>> mal = MAL()
>>> anime = mal.get_anime(1575)
>>> anime.fetched
False
>>> anime.fetch()
>>> anime.fetched
True

>>> anime.aired
{'Aired_end': datetime.date(2007, 7, 28), 'Aired_start': datetime.date(2006, 10, 6), 'Season': ('Fall', 2006)}
>>> anime.title
'Code Geass: Hangyaku no Lelouch'
>>> anime.mal_id
1575

>>> from pprint import pprint
>>> pprint(anime.__dict__)
{'aired': {'Aired_end': datetime.date(2007, 7, 28),
           'Aired_start': datetime.date(2006, 10, 6),
           'Season': ('Fall', 2006)},
 'alternative_titles': {'English': ['Code Geass: Lelouch of the Rebellion'],
                        'Japanese': [u'\u30b3\u30fc\u30c9\u30ae\u30a2\u30b9 \u53cd\u9006\u306e\u30eb\u30eb\u30fc\u30b7\u30e5']},
 'cover': 'http://cdn.myanimelist.net/images/anime/12/14327.jpg',
 'fetched': True,
 'info': {'Aired': 'Oct  6, 2006 to Jul  28, 2007',
          'Duration': 24,
          'Episodes': 25,
          'Genres': [{'id': 1, 'name': 'Action'},
                     {'id': 18, 'name': 'Mecha'},
                     {'id': 23, 'name': 'School'},
                     {'id': 24, 'name': 'Sci-Fi'},
                     {'id': 31, 'name': 'Super Power'},
                     {'id': 38, 'name': 'Military'}],
          'Producers': [{'id': 14, 'name': 'Sunrise'},
                        {'id': 143, 'name': 'Mainichi Broadcasting'},
                        {'id': 233, 'name': 'Bandai Entertainment'},
                        {'id': 757, 'name': 'Sony Music Entertainment'}],
          'Rating': 'R+ - Mild Nudity',
          'Status': 'Finished Airing',
          'Type': 'TV'},
 'mal': <malparser.mal.MAL object at 0xb750a8ac>,
 'mal_id': 1575,
 'related': {'Adaptation': [Manga(mal_id=1528), Manga(mal_id=11496)],
             'Other': [Anime(mal_id=8888)],
             'Sequel': [Anime(mal_id=2904)],
             'Side story': [Anime(mal_id=1953)],
             'Spin-off': [Anime(mal_id=12685), Anime(mal_id=17277)],
             'Summary': [Anime(mal_id=2124), Anime(mal_id=4596)]},
 'statistics': {'Favorites': 22386,
                'Members': 240569,
                'Popularity': 3,
                'Ranked': 12,
                'Score': Decimal('8.88'),
                'Votes': 170114},
 'synopsis': "On August 10th of the year 2010 the Holy Empire of Britannia began a campaign of conquest, its sights set on Japan. Operations were completed in one month thanks to Britannia's deployment of new mobile humanoid armor vehicles dubbed Knightmare Frames. Japan's rights and identity were stripped away, the once proud nation now referred to as Area 11. Its citizens, Elevens, are forced to scratch out a living while the Britannian aristocracy lives comfortably within their settlements. Pockets of resistance appear throughout Area 11, working towards independence for Japan.",
 'title': 'Code Geass: Hangyaku no Lelouch'}

>>> sequel_anime = anime.related_anime['Sequel'][0]
>>> sequel_anime.fetched
False
>>> sequel_anime.fetch()
>>> sequel_anime.fetched
True
>>> sequel_anime.title
'Code Geass: Hangyaku no Lelouch R2'

>>> manga = mal.get_manga(1528)
>>> manga.fetch()
>>> pprint(manga.__dict__)
{'alternative_titles': {'English': ['Code Geass: Lelouch of the Rebellion'],
                        'Japanese': [u'\u30b3\u30fc\u30c9\u30ae\u30a2\u30b9 \u53cd\u9006\u306e\u30eb\u30eb\u30fc\u30b7\u30e5']},
 'cover': 'http://cdn.myanimelist.net/images/manga/5/27730.jpg',
 'fetched': True,
 'info': {'Authors': [{'id': 3066, 'name': 'Taniguchi, Goro'},
                      {'id': 3067, 'name': 'Okouchi, Ichiro'},
                      {'id': 3081, 'name': 'Majiko!'}],
          'Chapters': 38,
          'Genres': [{'id': 1, 'name': 'Action'},
                     {'id': 8, 'name': 'Drama'},
                     {'id': 18, 'name': 'Mecha'},
                     {'id': 23, 'name': 'School'},
                     {'id': 24, 'name': 'Sci-Fi'},
                     {'id': 25, 'name': 'Shoujo'},
                     {'id': 37, 'name': 'Supernatural'},
                     {'id': 38, 'name': 'Military'}],
          'Published': 'Oct 2006 to 2010',
          'Serialization': [{'id': 14, 'name': 'Asuka (Monthly)'}],
          'Status': 'Finished',
          'Type': 'Manga',
          'Volumes': 8},
 'mal': <malparser.mal.MAL object at 0xb750a8ac>,
 'mal_id': 1528,
 'related': {'Adaptation': [Anime(mal_id=1575), Anime(mal_id=2904)],
             'Alternative setting': [Manga(mal_id=10167),
                                     Manga(mal_id=25854)],
             'Alternative version': [Manga(mal_id=1547),
                                     Manga(mal_id=1530),
                                     Manga(mal_id=11496)],
             'Prequel': [Manga(mal_id=17311)],
             'Spin-off': [Manga(mal_id=11968),
                          Manga(mal_id=12042),
                          Manga(mal_id=10822)]},
 'statistics': {'Favorites': 367,
                'Members': 6923,
                'Popularity': 293,
                'Ranked': 2109,
                'Score': Decimal('7.74'),
                'Votes': 3180},
 'synopsis': "The Empire of Brittania has invaded Japan using giant robot weapons called Knightmare Frames. Japan is now referred to as Area 11, and its people the 11s. A Brittanian who was living in Japan at the time, Lelouch, vowed to his Japanese friend Suzaku that he'd destroy Brittania. Years later, Lelouch is in high school, but regularly skips out of school to go play chess and gamble on himself.",
 'title': 'Code Geass: Hangyaku no Lelouch'}
```

I want to use my own http client, aka. how do I use this with [Twisted]

```python
from twisted.internet import defer
from twisted.web.client import getPage

from malparser import MAL

class TwistedMAL(MAL):
    @defer.inlineCallbacks
    def _fetch(self, obj):
        data = yield getPage(obj._get_url())
        obj.parse(data)
```

And how do i use that?
```python
>>> from twisted.internet import reactor
>>> twistedmal = TwistedMAL()
>>> anime = twistedmal.get_anime(1575)
>>> anime.fetch().addCallback(lambda x:reactor.stop())
>>> reactor.run()
>>> anime.fetched
True
```

Requirements
------------

* [lxml]

More stuff and contact
----------------------
See http://github.com/JohnDoee for anything you might need

Versioning
----------
Follows: [Semantic Versioning]

License
--------
See LICENSE

[lxml]: http://lxml.de/
[MyAnimeList]: http://myanimelist.net
[Twisted]: http://twistedmatrix.com/
[Semantic Versioning]: http://semver.org/