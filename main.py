__author__ = 'Skimmerzzz'

import logging
import newscrawler
import sys
from datetime import datetime


def main():
    def print_help():
        print('Использование: \n'
              '\t --help    Данная страница помощи\n'
              '\t -h\n'
              '\t\t то же самое, что и --help\n'
              '\t --bypage\n'
              '\t\t Получить все новости для указанной категории и региона. '
              'Регионов может быть указано несколько. Категория - только одна\n'
              '\t\t Сначала укажите категорию, затем все необходимые ОКТМО коды регионов\n'
              '\t\t Пример: Получить все новости для Москвы и Алтайского края в категории "финансы"\n'
              '\t\t     PROGNAME --bypage finance 45 1\n'
              '\t -p\n'
              '\t\t то же самое, что и --bypage'
              '\t --count\n'
              '\t\t Вывести количество новостей для всех регионов указанной категории.\n'
              '\t\t Пример: Вывести количество новостей по всем регионам в категории "финансы\n"'
              '\t\t     PROGNAME --count finance\n'
              '\t -c\n'
              '\t\t то же самое, что и --count\n'
              '\t --pagenum\n'
              '\t\t Вывести количество страниц новостей для всех регионов указанной категории.\n'
              '\t\t Пример: Вывести количество страниц по всем регионам в категории "финансы\n"'
              '\t\t     PROGNAME --pagenum finance\n'
              '\t -n\n'
              '\t\t то же самое, что и --pagenum\n')

        print_regions_codes()
        print('')
        print_categories()

    def print_regions_codes():
        print('Допустимые коды регионов:')
        print(newscrawler.get_all_regions_codes())

    def print_categories():
        print('Допустимые категории:')
        print(newscrawler.get_all_categories())

    arguments = sys.argv

    if len(arguments) < 2:
        print('Отсутствуют параметры.')
        print_help()
        sys.exit()

    if arguments[1] == '-h' or arguments[1] == '--help':
        print_help()
    elif arguments[1] == '-p' or arguments[1] == '--bypage':
        if len(arguments) < 3:
            print('Неверные параметры. Укажите категорию, затем коды регионов.')
            print_help()
            sys.exit()

        category = arguments[2]
        if category in newscrawler.get_all_categories():

            if len(arguments) < 4:
                print('Неверные параметры. Укажите коды регионов.')
                print_help()
                sys.exit()

            regions = arguments[3:]

            # finance, 41 region - only 2 pages!

            for region in regions:
                if region in newscrawler.get_all_regions_codes():
                    print('Получаем новости для региона {0}'.format(newscrawler.get_region_name_by_oktmo(region)[0]))
                    print('=' * 50)
                    cr = newscrawler.ArchiveCrawlerBezformataRu()

                    min_page = 1
                    try:
                        max_page = int(cr.get_max_page_number(region, category))
                    except TypeError:
                        print('Для региона {0}, категории {1} нет доступных новостей'.format(region, category))
                        continue
                    print('Для региона с кодом {0} имеется {1} страниц со ссылками на новости. '
                          'Начинаем обработку...'.format(region, str(max_page)))

                    news = cr.get_news_by_category_n_page(region, category, min_page, max_page)

                    wr = newscrawler.FileWriter()
                    wr.write_news_list(region + '-' + category + '-' + str(min_page) + '-' + str(max_page), news)

                else:
                    print('Неверный код региона: {0}'.format(region))
                    print('Пропускаем, переходим к следующему...')
                    #print_regions_codes()
                    #sys.exit()
                    continue

        else:
            print('Категория указана неверно.')
            print_categories()
            sys.exit()

    elif arguments[1] == '-c' or arguments[1] == '--count':
        if len(arguments) < 3:
            print('Неверные параметры. Укажите категорию.')
            print_help()
            sys.exit()

        category = arguments[2]
        if category in newscrawler.get_all_categories():
            print('Количество новостей категории {0} по всем регионам:'.format(category))
            print('=' * 50)

            cr = newscrawler.ArchiveCrawlerBezformataRu()

            for region in sorted(newscrawler.get_all_regions_codes()):
                print('Регион: {0}. Новостей: {1}'.format(region, cr.get_news_links_number(region, category)))
        else:
            print('Категория указана неверно.')
            print_categories()
            sys.exit()

    elif arguments[1] == '-n' or arguments[1] == '--pagenum':
        if len(arguments) < 3:
            print('Неверные параметры. Укажите категорию.')
            print_help()
            sys.exit()

        category = arguments[2]
        if category in newscrawler.get_all_categories():
            print('Количество страниц новостей для категории {0} по всем регионам:'.format(category))
            print('=' * 50)
            print('Текущее время: {0}'.format(datetime.now()))
            print('=' * 50)

            cr = newscrawler.ArchiveCrawlerBezformataRu()

            for region in sorted(newscrawler.get_all_regions_codes()):
                print('Регион: {0}. Страниц: {1}'.format(region, cr.get_max_page_number(region, category)))

        else:
            print('Категория указана неверно.')
            print_categories()
            sys.exit()

    else:
        print('Неверные параметры.')
        print_help()
        sys.exit()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    main()
