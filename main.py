__author__ = 'Skimmerzzz'

import logging
import newscrawler
import sys
import os
from datetime import datetime
from optparse import OptionParser

def main():

    """
        def print_help():

            PROGNAME = os.path.basename(sys.argv[0])

            print('Использование: \n'
                  '\t --help    Данная страница помощи\n'
                  '\t -h\n'
                  '\t\t то же самое, что и --help\n'
                  '\t --bypage\n'
                  '\t\t Получить все новости для указанной категории и региона. '
                  'Регионов может быть указано несколько. Категория - только одна.\n'
                  '\t\t Сначала укажите категорию, затем все необходимые ОКТМО коды регионов\n'
                  '\t\t Пример: Получить все новости для Москвы и Алтайского края в категории "финансы"\n'
                  '\t\t     {0} --bypage finance 45 1\n'
                  '\t -p\n'
                  '\t\t то же самое, что и --bypage\n'
                  '\t --bypagenum\n'
                  '\t\t Получить новости определенных страниц для указанных категории, региона. '
                  'Регион - только один. Категория - только одна\n'
                  '\t\t Сначала укажите категорию, затем ОКТМО код региона.\n'
                  '\t\t Далее диапазон страниц для загрузки.\n'
                  '\t\t Пример: Получить все новости для Москвы в категории "финансы" со второй по десятую страницы\n'
                  '\t\t     {0} --bypage finance 45 2 10\n'
                  '\t -pn\n'
                  '\t\t то же самое, что и --bypagenum\n'
                  '\t --count\n'
                  '\t\t Вывести количество новостей для всех регионов указанной категории.\n'
                  '\t\t Пример: Вывести количество новостей по всем регионам в категории "финансы"\n'
                  '\t\t     {0} --count finance\n'
                  '\t -c\n'
                  '\t\t то же самое, что и --count\n'
                  '\t --pagenum\n'
                  '\t\t Вывести количество страниц новостей для всех регионов указанной категории.\n'
                  '\t\t Пример: Вывести количество страниц по всем регионам в категории "финансы"\n'
                  '\t\t     {0} --pagenum finance\n'
                  '\t -n\n'
                  '\t\t то же самое, что и --pagenum\n'.format(PROGNAME))

            print_regions_codes()
            print('')
            print_categories()

        def print_regions_codes():
            print('Допустимые коды регионов:')
            print(newscrawler.get_all_regions_codes())

        def print_categories():
            print('Допустимые категории:')
            print(newscrawler.get_all_categories())
    """

    usage = "%prog [options] категория регион1 [регион2... регионN]"
    description = "Получение новостей с сайта bezformata.ru."
    version = "%prog 1.0"
    parser = OptionParser(usage=usage, description=description, version=version)

    # The second option value is bydate.

    parser.add_option("-t","--type", dest="crawling_type", help="Режим получения новостей с сайта: по дате (bydate), по страницам (bypage)."
                                                                "По умолчанию в постраничном режиме."
                                                                "Фиксируется категория, регион, "
                                                                "перебираются страницы новостей."
                                                                "Режим bydate не реализован.")

    parser.add_option("-a", "--action", dest="action", help="Действие: получить новости (getnews), посчитать страницы"
                                                            "(countpages), посчитать новости (countnews).")

    # TODO Опция номеров страниц? Или две...
    # TODO FileWriter умеет принимать рабочую папку на вход. Опция?
    # TODO логгирование в файл. Опция?

    parser.set_defaults(crawling_type="bypage")
    parser.set_defaults(action="getnews")

    test_args=["-h", "--version"]
    (options, args) = parser.parse_args(test_args)
    print(options)
    print(args)

"""
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

    elif arguments[1] == '-pn' or arguments[1] == '--bypagenum':
        if len(arguments) < 3:
            print('Неверные параметры. Укажите категорию, затем код региона, диапазон страниц для загрузки.')
            print_help()
            sys.exit()

        category = arguments[2]
        if category in newscrawler.get_all_categories():

            if len(arguments) < 4:
                print('Неверные параметры. Укажите код региона, диапазон страниц для загрузки.')
                print_help()
                sys.exit()

            region = arguments[3]

            if len(arguments) < 6:
                print('Неверные параметры. Укажите диапазон страниц для загрузки.')
                print_help()
                sys.exit()

            try:
                min_page = int(arguments[4])
                max_page = int(arguments[5])
            except TypeError:
                print('Неверно указан диапазон страниц для загрузки.')
                print_help()
                sys.exit()

            if max_page < min_page:
                print('Неверные параметры. Номер первой страницы диапазона для загрузки должен быть меньше или равен '
                      'номеру последней страницы.')
                print_help()
                sys.exit()

            if region in newscrawler.get_all_regions_codes():
                print('Получаем новости в категории {0} для региона {1} в диапазоне страниц '
                      'с {2} по {3}'.format(category, newscrawler.get_region_name_by_oktmo(region)[0],
                      min_page, max_page))
                print('=' * 50)
                cr = newscrawler.ArchiveCrawlerBezformataRu()

                news = cr.get_news_by_category_n_page(region, category, min_page, max_page)

                wr = newscrawler.FileWriter()
                wr.write_news_list(region + '-' + category + '-' + str(min_page) + '-' + str(max_page), news)

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
"""

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    main()
