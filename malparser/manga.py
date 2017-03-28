from malparser.base import Base

class Manga(Base):
    base_url = 'http://myanimelist.net/manga/%s/'
    
    #def parse(self, html):
    #    super(Anime, self).parse(html)
    #    
    #    self.aired = aired = {
    #        'Aired_start': None,
    #        'Aired_end': None,
    #        'Season': None,
    #    }
    #    
    #    if 'Aired' in self.info:
    #        if self.info['Aired'] != 'Not yet aired':
    #            if ' to ' in self.info['Aired']:
    #                aired['Aired_start'], aired['Aired_end'] = self.info['Aired'].split(' to ')
    #            else:
    #                aired['Aired_start'] = aired['Aired_end'] = self.info['Aired']
    #            
    #            aired['Aired_start'] = self.parse_date(aired['Aired_start'])
    #            aired['Aired_end'] = self.parse_date(aired['Aired_end'])
    #            
    #            aired['Season'] = self.get_season(aired['Aired_start'])

    def __repr__(self):
        return 'Manga(mal_id=%r)' % self.mal_id
    