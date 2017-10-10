import decimal
import re

import lxml.html


class Base(object):
    fetched = False

    def __init__(self, mal_id, mal):
        self.mal_id = mal_id
        self.mal = mal

    def _get_url(self):
        return self.base_url % self.mal_id

    def fetch(self):
        if not self.fetched:
            return self.mal._fetch(self)

    def parse(self, html):
        # Ignoring errors here because MAL allows users to use their own encodings
        # Without testing, probably allows the users to store pictures from their latest vacation as a review
        # Anyways, anything we need is (hopefully) in utf-8
        tree = lxml.html.fromstring(html)

        schema = tree.xpath('//div[@id="contentWrapper"]')[0]

        self.title = schema.xpath('.//span[@itemprop="name"]/text()')[0].strip()
        synopsis = schema.xpath('.//span[@itemprop="description"]//text()')
        if synopsis:
            self.synopsis = ''.join(synopsis)
        else:
            self.synopsis = ''
        self.cover = schema.xpath('.//img[@itemprop="image"]')[0]
        if 'data-src' in self.cover.attrib:
            self.cover = self.cover.attrib['data-src']
        else:
            self.cover = self.cover.attrib['src']

        self.info = info = {}
        self.alternative_titles = alternative_titles = {}
        self.statistics = statistics = {}
        self.related = related = {}
        self.reviews = []

        def duration2int(x):
            runtime = 0
            hours = re.findall(r'(\d+) hr', x)
            minutes = re.findall(r'(\d+) min', x)
            if hours:
                try:
                    runtime += int(hours[0])*60
                except ValueError:
                    pass

            if minutes:
                try:
                    runtime += int(minutes[0])
                except ValueError:
                    pass

            return runtime

        def num2int(x):
            try:
                return int(x.replace(',', ''))
            except ValueError:
                return None

        def num2dec(x):
            try:
                return decimal.Decimal(x)
            except decimal.InvalidOperation:
                return None

        strip2int = lambda x: x != 'N/A' and int(x.strip('#')) or None

        loop_elements = [
            ('Alternative Titles', True, [], alternative_titles, {}),
            ('Information', False, ['Producers', 'Genres', 'Authors', 'Serialization', 'Licensors', 'Studios'], info, {'Episodes': num2int, 'Duration': duration2int, 'Volumes': num2int, 'Chapters': num2int}),
            ('Statistics', False, [], statistics, {'Favorites': num2int, 'Members': num2int, 'Popularity': strip2int, 'Ranked': strip2int}),
        ]

        for block, splitlist, linklist, save_target, postprocess in loop_elements:
            for el in tree.xpath('//h2[text()="%s"]/following-sibling::*' % block):
                if el.tag != 'div' or not el.xpath('span') or ':' not in el.xpath('span/text()')[0]:
                    break

                text = ''.join(el.xpath('text()')).strip()
                info_type = el.xpath('span/text()')[0].strip(':')
                if info_type in linklist:
                    save_target[info_type] = []

                    if 'None found' not in text:
                        for a in el.xpath('a'):
                            save_target[info_type].append({
                                'id': int(re.findall('\d+', a.attrib['href'])[-1]),
                                'name': a.text
                            })
                elif info_type == 'Type':
                    types_found = sorted(el.xpath('.//a/text()'), key=lambda x:len(x))
                    if not types_found:
                        types_found = sorted(el.xpath('.//text()'), key=lambda x:len(x))

                    if types_found:
                        types_found = [str(x).strip() for x in types_found if str(x).strip() and str(x).strip() != 'Type:']
                        if types_found:
                            save_target[info_type] = str(types_found[-1])
                elif info_type == 'Premiered':
                    premiered = el.xpath('./a/text()')[0].split(' ')
                    if premiered:
                        year = premiered[1]
                        try:
                            year = int(premiered[1])
                        except ValueError:
                            pass

                        save_target[info_type] = {
                            'season': premiered[0],
                            'year': year,
                        }
                else:
                    save_target[info_type] = text.strip()
                    if splitlist:
                        save_target[info_type] = [x.strip() for x in save_target[info_type].split(',')]
                    elif info_type in postprocess:
                        save_target[info_type] = postprocess[info_type](save_target[info_type])


        score_box = tree.xpath('//div[./span[text()="Score:"]]/span')

        votes = tree.xpath('//span[@itemprop="ratingCount"]/text()')
        if votes:
            statistics['Votes'] = votes[0]
        else:
            statistics['Votes'] = score_box[2].xpath('./text()')[0]

        if 'Votes' in statistics:
            statistics['Votes'] = int(statistics['Votes'].replace(',', ''))

        score = tree.xpath('//span[@itemprop="ratingValue"]/text()')
        if score:
            statistics['Score'] = score[0]
        else:
            statistics['Score'] = score_box[1].xpath('./text()')[0]

        if 'Score' in statistics:
            statistics['Score'] = num2dec(statistics['Score'])

        for el in tree.xpath('//table[@class="anime_detail_related_anime"]/tr'):
            name, relationships = el.xpath('./td')
            name = name.text.strip(':')
            related[name] = []
            for r in relationships.xpath('./a'):
                url = r.attrib['href'].split('/')
                tag_type = url[1]
                tag_id = url[2]
                related[name].append({'type': tag_type, 'id': int(tag_id)})

        self.mal._handle_related(self)

        for review in tree.xpath('//h2[contains(text(), "Reviews")]/following-sibling::*//div[contains(@class, "borderLight")]'):
            rating = int(review.xpath('.//a[text()="Overall Rating"]/../text()')[0].strip(': '))
            review = ''.join(review.xpath('following-sibling::div/text()')).strip() + '\n'.join(review.xpath('following-sibling::div/span/text()')).strip()
            review = review.replace('\n\n', '\n')

            self.reviews.append({
                'rating': rating,
                'review': review
            })

        self.fetched = True
