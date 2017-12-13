from .base import Base


class Manga(Base):  # not implemented yet
    base_url = 'http://myanimelist.net/manga/%s/'

    def __repr__(self):
        return 'Manga(mal_id=%r)' % self.mal_id
