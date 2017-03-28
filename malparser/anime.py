import urllib
import re
from decimal import Decimal
from datetime import datetime

from malparser.base import Base

class Anime(Base):
    base_url = 'http://myanimelist.net/anime/%s/'
    
    def parse_date(self, d):
        if '?' in d:
            return None
        
        d = d.strip()
        if d != 'Not available':
            spaces = len(d.split(' '))
            if spaces == 1:
                return datetime.strptime(d, '%Y').date()
            elif spaces == 2:
                return datetime.strptime(d, '%b, %Y').date()
            else:
                return datetime.strptime(d, '%b  %d, %Y').date()
    
    def get_season(self, d):
        if d.month in [2, 3, 4]:
            return ('Spring', d.year)
        elif d.month in [5, 6, 7]:
            return ('Summer', d.year)
        elif d.month in [8, 9, 10]:
            return ('Fall', d.year)
        else:
            return ('Winter', d.year)
    
    def parse(self, html):
        super(Anime, self).parse(html)
        
        self.aired = aired = {
            'Aired_start': None,
            'Aired_end': None,
            'Season': None,
        }
        
        if 'Aired' in self.info:
            if self.info['Aired'] != 'Not yet aired':
                if ' to ' in self.info['Aired']:
                    aired['Aired_start'], aired['Aired_end'] = self.info['Aired'].split(' to ')
                else:
                    aired['Aired_start'] = aired['Aired_end'] = self.info['Aired']
                
                aired['Aired_start'] = self.parse_date(aired['Aired_start'])
                aired['Aired_end'] = self.parse_date(aired['Aired_end'])
                
                if aired['Aired_start']:
                    aired['Season'] = self.get_season(aired['Aired_start'])

    def __repr__(self):
        return 'Anime(mal_id=%r)' % self.mal_id
    