__author__ = 'Skimmerzzz'

import logging
import newscrawler
import datetime


def main():

    start_date = datetime.date(2015, 4, 20)
    end_date = datetime.date(2015, 4, 20)
    cr = newscrawler.ArchiveCrawlerBezformataRu()
    # TODO Make a dictionary may be
    news = cr.get_region_news('moskva', start_date, end_date)

    print(news)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    main()
