__author__ = 'Skimmerzzz'

import logging
import newscrawler
import sys


def main():

    def print_help():
        print('Usage: \n'
              '\t -h    This help\n'
              '\t --bypage\n'
              '\t\t Fetch all news for specified category and regions\n'
              '\t\t Set category first, then all regions OKTMO codes\n'
              '\t\t Example: fetch all news for Moscow and Altaiskiy krai, finance category\n'
              '\t\t     PROGNAME --bypage finance 45 1\n'
              '\t -p\n'
              '\t\t the same as --bypage')

        print_regions_codes()
        print('')
        print_categories()

    def print_regions_codes():
        print('Possible region codes:')
        print(newscrawler.get_all_regions_codes())

    def print_categories():
        print('Possible categories:')
        print(newscrawler.get_all_categories())

    arguments = sys.argv

    if len(arguments) < 2:
        print('Incorrect usage.')
        print_help()
        sys.exit()

    if arguments[1] == '-h' or arguments[1] == '--help':
        print_help()
    elif arguments[1] == '-p' or arguments[1] == '--bypage':
        if len(arguments) < 3:
            print('Incorrect usage.')
            print_help()
            sys.exit()

        category = arguments[2]
        if category in newscrawler.get_all_categories():
            print('Correct category')

            if len(arguments) < 4:
                print('Incorrect usage. Please set region codes')
                print_help()
                sys.exit()

            regions = arguments[3:]

            # finance, 41 region - only 2 pages!

            for region in regions:
                if region in newscrawler.get_all_regions_codes():
                    print('Получаем новости для региона {0}'.format(newscrawler.get_region_name_by_oktmo(region)[0]))
                    print('='*40)
                    cr = newscrawler.ArchiveCrawlerBezformataRu()

                    min_page = 1
                    try:
                        max_page = int(cr.get_max_page_number(region, category))
                    except TypeError:
                        print('Для региона {0}, категории {1} нет доступных новостей'.format(region, category))
                        continue
                    print('=== max_page is ' + str(max_page))

                    news = cr.get_news_by_category_n_page(region, category, min_page, max_page)

                    wr = newscrawler.FileWriter()
                    wr.write_news_list(region + '-' + category + '-' + str(min_page) + '-' + str(max_page), news)

                else:
                    print('Incorrect region.')
                    print_regions_codes()
                    sys.exit()



        else:
            print('Incorrect category')
            print_categories()
            sys.exit()

    else:
        print('Incorrect usage.')
        print_help()
        sys.exit()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    main()
