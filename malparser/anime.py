from .base import Base


class Anime(Base):
    base_url = 'https://myanimelist.net/anime/%s/'

    def reset(self):
        super(Anime, self).reset()

        self.aired = {
            'Aired_start': None,
            'Aired_end': None,
            'Season': None,
        }

    def parse(self, html):
        super(Anime, self).parse(html)

        aired = self.aired

        if 'Aired' in self.info:
            aired['Aired_start'], aired['Aired_end'], aired['Season'] = self.convert_aired_dates(self.info['Aired'])

    def __repr__(self):
        return 'Anime(mal_id=%r)' % self.mal_id
