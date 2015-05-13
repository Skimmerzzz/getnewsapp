__author__ = 'Skimmerzzz'

import logging
import newscrawler
import datetime


def main():

    start_date = datetime.date(2015, 4, 20)
    end_date = datetime.date(2015, 4, 20)
    cr = newscrawler.ArchiveCrawlerBezformataRu()
    # TODO Make a dictionary may be
    #news = cr.get_region_news('45', start_date, end_date)
    news = cr.get_region_news('45')
    wr = newscrawler.FileWriter()
    wr.write_news_list(news)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    main()
