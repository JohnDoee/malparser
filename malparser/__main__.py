import argparse

from pprint import pprint

def main():
    parser = argparse.ArgumentParser(description='Fetch info from IMDb')
    parser.add_argument('mal_id', help='a MAL id, e.g. 1575')

    args = parser.parse_args()

    from .mal import MAL
    i = MAL()
    anime = i.get_anime(args.mal_id)
    anime.fetch()
    pprint(anime.__dict__)


if __name__ == '__main__':
    main()
