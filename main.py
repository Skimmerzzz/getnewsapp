__author__ = 'Skimmerzzz'

import logging
import newscrawler
import datetime


def main():

    """
    start_date = datetime.date(2015, 4, 20)
    end_date = datetime.date(2015, 4, 20)
    cr = newscrawler.ArchiveCrawlerBezformataRu()
    # TODO Make a dictionary may be
    #news = cr.get_news_by_region_n_time('45', start_date, end_date)
    news = cr.get_news_by_region_n_time('45')

    """

    # TODO Make tests
    #test = newscrawler.get_all_categories()
    #test = newscrawler.get_all_regions_codes()
    #print(test)

    category = 'finance'
    region = '1'

    cr = newscrawler.ArchiveCrawlerBezformataRu()
    """
    min_page = 1
    max_page = cr.get_max_page_number(region, category)
    print('=== max_page is ' + str(max_page))

    news = cr.get_news_by_category_n_page(region, category, min_page, max_page)

    wr = newscrawler.FileWriter()
    wr.write_news_list(region + '-' + category + '-' + str(min_page) + '-' + str(max_page), news)"""

    # ['8', '10', '11', '12']
    # ['14', '15', '17', '18', '19', '20']
    # ['24', '25', '27', '29', '32', '33', '34', '37', '38']
    # '41', '42', '44', '46', '47',
    # '49', '50', '52', '53', '54', '56', '58', '22'
    # '60', '61', '36', '63', '64', '65', '66', '68', '69', '28'

    for region in []:
        min_page = 1
        max_page = int(cr.get_max_page_number(region, category))
        print('=== max_page is ' + str(max_page))

        news = cr.get_news_by_category_n_page(region, category, min_page, max_page)

        wr = newscrawler.FileWriter()
        wr.write_news_list(region + '-' + category + '-' + str(min_page) + '-' + str(max_page), news)

    """for region in newscrawler._REGIONS_BY_OKTMO_DIC:
        min_page = 1
        max_page = int(cr.get_max_page_number(region, category))
        print('=== max_page is ' + str(max_page))

        news = cr.get_news_by_category_n_page(region, category, min_page, max_page)

        wr = newscrawler.FileWriter()
        wr.write_news_list(region + '-' + category + '-' + str(min_page) + '-' + str(max_page), news)
    """

    #news = cr.get_news_by_category_n_page()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    main()
