__author__ = 'Skimmerzzz'

import logging

import datetime
import time

import urllib.request
import urllib.error
import re
import urllib.parse

import os
import csv

import hashlib

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# logger.setLevel(logging.DEBUG)

_CATEGORIES_LIST = ['society', 'sport', 'kultura', 'religion', 'incident', 'event', 'poll', 'science', 'politic',
                    'state', 'army', 'city', 'region', 'projects', 'conquest', 'expo', 'economics', 'finance',
                    'energetics', 'eco', 'health', 'realty', 'transport', 'communication', 'internet',
                    'peoples', 'reporter', 'report', 'cutoff', 'horoscope']

_REGIONS_BY_OKTMO_DIC = {'79': ('Республика Адыгея', 'maikop'),
                         '84': ('Республика Алтай', 'gornoaltaysk'),
                         '80': ('Республика Башкортостан', 'ufa'),
                         '81': ('Республика Бурятия', 'ulanude'),
                         '82': ('Республика Дагестан', 'mahachkala'),
                         '26': ('Республика Ингушетия', 'magas'),
                         '83': ('Кабардино-Балкарская республика', 'nalchik'),
                         '85': ('Республика Калмыкия', 'elista'),
                         '91': ('Карачаево-Черкесская республика', 'cherkesk'),
                         '86': ('Республика Карелия', 'petrozavodsk'),
                         '87': ('Республика Коми', 'siktivkar'),
                         '35': ('Республика Крым', 'simferopol'),
                         '88': ('Республика Марий Эл', 'yoshkarola'),
                         '89': ('Республика Мордовия', 'saransk'),
                         '98': ('Республика Саха (Якутия)', 'yakutsk'),
                         '90': ('Республика Северная Осетия — Алания', 'vladikavkaz'),
                         '92': ('Республика Татарстан', 'kazan'),
                         '93': ('Республика Тыва', 'kizil'),
                         '94': ('Удмуртская республика', 'ijevsk'),
                         '95': ('Республика Хакасия', 'abakan'),
                         '96': ('Чеченская республика', 'grozniy'),
                         '97': ('Чувашская республика', 'cheboksari'),
                         '1': ('Алтайский край', 'barnaul'),
                         '76': ('Забайкальский край', 'chita'),
                         '30': ('Камчатский край', 'petropavlovskkamchatskiy'),
                         '3': ('Краснодарский край', 'krasnodar'),
                         '4': ('Красноярский край', 'krasnoyarsk'),
                         '57': ('Пермский край', 'perm'),
                         '5': ('Приморский край', 'vladivostok'),
                         '7': ('Ставропольский край', 'stavropol'),
                         '8': ('Хабаровский край', 'habarovsk'),
                         '10': ('Амурская область', 'blagoveshensk'),
                         '11': ('Архангельская область', 'arhangelsk'),
                         '12': ('Астраханская область', 'astrahan'),
                         '14': ('Белгородская область', 'belgorod'),
                         '15': ('Брянская область', 'bryansk'),
                         '17': ('Владимирская область', 'vladimir'),
                         '18': ('Волгоградская область', 'volgograd'),
                         '19': ('Вологодская область', 'vologda'),
                         '20': ('Воронежская область', 'voronej'),
                         '24': ('Ивановская область', 'ivanovo'),
                         '25': ('Иркутская область', 'irkutsk'),
                         '27': ('Калининградская область', 'kaliningrad'),
                         '29': ('Калужская область', 'kaluga'),
                         '32': ('Кемеровская область', 'kemerovo'),
                         '33': ('Кировская область', 'kirov'),
                         '34': ('Костромская область', 'kostroma'),
                         '37': ('Курганская область', 'kurgan'),
                         '38': ('Курская область', 'kursk'),
                         '41': ('Ленинградская область', 'lenoblast'),
                         '42': ('Липецкая область', 'lipeck'),
                         '44': ('Магаданская область', 'magadan'),
                         '46': ('Московская область', 'podmoskovye'),
                         '47': ('Мурманская область', 'murmansk'),
                         '22': ('Нижегородская область', 'nnovgorod'),
                         '49': ('Новгородская область', 'velikiynovgorod'),
                         '50': ('Новосибирская область', 'novosibirsk'),
                         '52': ('Омская область', 'omsk'),
                         '53': ('Оренбургская область', 'orenburg'),
                         '54': ('Орловская область', 'orel'),
                         '56': ('Пензенская область', 'penza'),
                         '58': ('Псковская область', 'pskov'),
                         '60': ('Ростовская область', 'rostovnadonu'),
                         '61': ('Рязанская область', 'ryazan'),
                         '36': ('Самарская область', 'samara'),
                         '63': ('Саратовская область', 'saratov'),
                         '64': ('Сахалинская область', 'ujnosahalinsk'),
                         '65': ('Свердловская область', 'ekaterinburg'),
                         '66': ('Смоленская область', 'smolensk'),
                         '68': ('Тамбовская область', 'tambov'),
                         '28': ('Тверская область', 'tver'),
                         '69': ('Томская область', 'tomsk'),
                         '70': ('Тульская область', 'tula'),
                         '71': ('Тюменская область', 'tumen'),
                         '73': ('Ульяновская область', 'uliyanovsk'),
                         '75': ('Челябинская область', 'chelyabinsk'),
                         '78': ('Ярославская область', 'yaroslavl'),
                         '45': ('Москва', 'moskva'),
                         '40': ('Санкт-Петербург', 'sanktpeterburg'),
                         '67': ('Севастополь', 'sevastopol'),
                         '99': ('Еврейская автономная область', 'birobidjan'),
                         '11-8': ('Ненецкий автономный округ', 'narianmar'),
                         '71-8': ('Ханты-Мансийский автономный округ - Югра', 'hantimansiysk'),
                         '77': ('Чукотский автономный округ', 'anadir'),
                         '71-9': ('Ямало-Ненецкий автономный округ', 'salehard')}


def get_all_categories():
    """
    :return: list of all categories
    """
    return _CATEGORIES_LIST


def get_all_regions_codes():
    """
    :return: list of all Bezformata.Ru codes
    """

    result = []

    for key in _REGIONS_BY_OKTMO_DIC:
        result.append(key)

    return result


def get_all_regions_mnemonic():
    """
    :return: list of all Bezformata.Ru codes
    """

    result = []

    for key in _REGIONS_BY_OKTMO_DIC:
        result.append(_REGIONS_BY_OKTMO_DIC[key][1])

    return result


def get_region_name_by_oktmo(oktmo_code):
    """

    :param oktmo_code:
    :return: Tuple (RegionName, BezformataRegionName, ...???)
    """
    return _REGIONS_BY_OKTMO_DIC[oktmo_code]


class NewsCrawler:
    """ Abstract crawler class
    """

    def __init__(self):
        self._crawler_type = None
        self._crawler_name = None

    @property
    def crawler_type(self):
        return self._crawler_type

    @property
    def crawler_name(self):
        return self._crawler_name

    @crawler_name.setter
    def crawler_name(self, value):
        self._crawler_name = value


class ArchiveCrawler(NewsCrawler):
    """ Crawler for structured news archives
    """

    def __init__(self):
        NewsCrawler.__init__(self)
        self._crawler_type = 'archive'
        self._start_date = datetime.date(1999, 1, 1)
        self._end_date = datetime.date.today()
        self._query_timeout = 0.5

        logger.debug("Archive crawler instance created")

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, value):
        self._start_date = value

    @property
    def end_date(self):
        return self._end_date

    @end_date.setter
    def end_date(self, value):
        self._end_date = value

    @property
    def query_timeout(self):
        return self._query_timeout


class ArchiveCrawlerBezformataRu(ArchiveCrawler):
    """  ArchiveCrawlerBezformataRu
    """

    _main_hostname = 'bezformata.ru'

    def __init__(self, start_date=datetime.date.today(), end_date=datetime.date.today()):

        ArchiveCrawler.__init__(self)
        self._crawler_name = 'BezformataRu'
        self._start_date = start_date
        self._end_date = end_date

    def get_news_by_region_n_time(self, region, start_date=datetime.date.today(), end_date=datetime.date.today()):
        """ Получить новости региона в заданном диапазоне дат.
        :param region: Регион, для которого получаем новости
        :param start_date:
        :param end_date:
        :return: Список объектов новостей NewsArticle
        """

        logger.debug(' get_news_by_region_n_time - IN')

        current_date = start_date
        news_list = []

        while current_date <= end_date:
            # Получаем список ссылок новостей для заданных даты и региона
            logger.info("Fetching news' links for %s region, %s date" % (
                get_region_name_by_oktmo(region)[0], str(current_date)))

            news_links_list = self._get_news_links_by_date(region, current_date)

            # TODO # Remove duplicates like in get_news_by_category_n_page
            logger.info("Fetching %d news' links to pages for %s region, %s date" % (
                len(news_links_list), get_region_name_by_oktmo(region)[0], str(current_date)))

            for link in news_links_list:
                news_article = self._get_news_article(self._crawler_type, self._crawler_name, region, link)
                if news_article is None:
                    continue
                else:
                    news_list.append(news_article)

                self._wait_after_news_fetching()

            current_date = current_date + datetime.timedelta(days=1)

        logger.info("Fetched %d news" % len(news_list))
        logger.debug(news_list)
        return news_list

    def get_max_page_number(self, region, category):
        """
        :param region:
        :param category:
        :return: max page number, Integer
        """

        logger.debug(' get_max_page_number - IN')

        # Site specific URL constants
        main_hostname = ArchiveCrawlerBezformataRu._main_hostname
        news_links_page_path = category
        news_page_path = '/listnews/'

        # TODO Rewrite get_region_name_by_oktmo(region)[1]
        # Url example 'http://moskva.bezformata.ru/economics/?npage=1'
        url = urllib.parse.urlunparse(('http', get_region_name_by_oktmo(region)[1] + '.' + main_hostname,
                                       news_links_page_path, '', '', ''))

        logger.debug(' get_max_page_number - Constructed URL: %s' % url)

        result = None

        try:
            data = urllib.request.urlopen(url)

            soup = BeautifulSoup(data)

            try:
                all_li = soup.find('div', attrs={'class': 'npage_box'}).find('ul', attrs={'id': 'nav-pages'})
                li_list = soup.find_all('li')
            except:
                logger.debug("get_max_page_number - Can't get min and max page numbers "
                             "for region {0} and category {1}".format(region, category))
                return None

            # TODO May be better iterate all and get by title='Последняя страница'
            # last_li = li_list[len(li_list)-1].next_element.attrs['title']

            last_li_text = li_list[len(li_list) - 1].next_element.attrs['href']

        except urllib.error.URLError as e:
            print(e.reason)

        searchObj = re.search(r'(.*)=(\d+)', last_li_text)
        result = searchObj.group(2)

        logger.debug(' get_max_page_number - OUT')

        return int(result)

    def get_news_links_number(self, region, category):
        """
        Считает количество ссылок для всех страниц заданных региона и категории
        :param region:
        :param category:
        :return: Integer
        """

        min_page = 1

        try:
            max_page = int(self.get_max_page_number(region, category))
        except TypeError:
            logger.debug("Для региона {0}, категории {1} нет страниц с сылками на новости".format(region, category))
            return 0

        news_links_list = []

        for current_page in range(min_page, max_page + 1):
            news_links_list += self._get_news_links_by_page(region, category, current_page)

        # Remove duplicates
        news_links_list = list(set(news_links_list))

        news_links_count = len(news_links_list)
        logger.debug('get_news_links_number: fetch {0} news links number for all pages of '
                     'the region {1} and category {2}'.format(news_links_count, region, category))

        return news_links_count

    def get_news_by_category_n_page(self, region, category, start_page, end_page):
        """ Возвращает список объектов новостей для заданных региона, категории и интервала страниц
        :param region: Регион, для которого получаем новости
        :param category: Категория, для которой получаем новости
        :param start_page: Номер перовый страницы для получения новостей
        :param end_page: Номер последней страницы для получения новостей
        :return: Список объектов новостей NewsArticle
        """

        logger.debug(' get_news_by_category_n_page - IN')

        current_page = start_page
        news_list = []
        news_links_list = []

        logger.info("Fetching news' links for %s region, %s category and %d end_page" % (
            get_region_name_by_oktmo(region)[0], category, end_page))

        while current_page <= end_page:
            # Получаем список ссылок новостей для заданных категории, страницы сайта и региона
            # logger.info("Fetching news' links for %s region, %s category and %d page" % (
            #   get_region_name_by_oktmo(region)[0], category, current_page))

            news_links_list = news_links_list + self._get_news_links_by_page(region, category, current_page)

            if current_page % 10 == 0:
                logger.info('current_page {0}'.format(current_page))

            current_page += 1

        # Remove duplicates
        news_links_list = list(set(news_links_list))

        logger.info("Fetched %d news' links for %s region, %s category and %d end_page" % (len(news_links_list),
                                                                                           get_region_name_by_oktmo(
                                                                                               region)[0], category,
                                                                                           end_page))

        counter = 0

        for link_item in enumerate(news_links_list):
            news_article = self._get_news_article(self._crawler_type, self._crawler_name, region, link_item[1],
                                                  category)
            if news_article is None:
                continue
            else:
                news_list.append(news_article)

            self._wait_after_news_fetching()

            if link_item[0] % 50 == 0:
                logger.info('link_idx {0}'.format(link_item[0]))

        logger.info("Fetched %d news" % len(news_list))
        logger.debug(news_list)
        return news_list

    def _get_news_links_by_page(self, region, category, page):
        """

        :param region: Регион
        :param category: Категория новости
        :param page: Номер страницы паджинации сайта
        :return: Список ссылок на новости
        """

        logger.debug(' _get_news_links_by_page - IN')

        # Site specific URL constants
        main_hostname = ArchiveCrawlerBezformataRu._main_hostname
        news_links_page_path = category
        news_page_path = '/listnews/'

        # Url example 'http://moskva.bezformata.ru/economics/?npage=1'
        url = urllib.parse.urlunparse(('http', get_region_name_by_oktmo(region)[1] + '.' + main_hostname,
                                       news_links_page_path, '', 'npage=' + str(page), ''))

        logger.debug(' _get_news_links_by_page - Constructed URL: %s' % url)

        links_list = []

        try:
            data = urllib.request.urlopen(url)

            soup = BeautifulSoup(data)

            # 'bezformata.ru/listnews/[^"]':
            # Fetch links to news articles only
            # Exclude main link by ^"

            # В режиме паджинации находит скрытые урлы из  div class=topic_box / div class=topicheader_box
            # Правая колонка новостей за сегодня. Вырезать позже.
            for link in soup.find_all('a', attrs={'href': re.compile(main_hostname + news_page_path + '[^"]')}):

                # Some links are duplicated (href for picture and new's title
                if link.get('href') not in links_list:
                    links_list.append(link.get('href'))

            logger.debug(' _get_news_links_by_page - Fetched links to pages: ' + str(links_list))

        except urllib.error.URLError as e:
            print(e.reason)

        logger.debug(' _get_news_links_by_page - OUT')

        # Links for unit-tests
        # ['http://moskva.bezformata.ru/listnews/obyazatelnogo-meditcinskogo-strahovaniya/33384150/']
        # ['http://moskva.bezformata.ru/listnews/himkah-muzhchina-otnyal-u-politcejskogo/32405548/']

        return links_list

    def _get_news_links_by_date(self, region, date):
        """ Получить ссылки на новости для заданных даты и региона
        :param region: Регион
        :param date: Дата
        :return: Список ссылок на новости для заданных даты и региона
        """

        logger.debug(' _get_news_links_by_date - IN')

        # Site specific URL constants
        main_hostname = ArchiveCrawlerBezformataRu._main_hostname
        news_links_page_path = '/daysnews/'
        news_page_path = '/listnews/'

        # Url example 'http://moskva.bezformata.ru/daynews/?nday=20&nmonth=4&nyear=2015'
        url = urllib.parse.urlunparse(('http', get_region_name_by_oktmo(region)[1] + '.' + main_hostname,
                                       news_links_page_path, '', 'nday=' + str(date.day) + '&nmonth='
                                       + str(date.month) + '&nyear=' + str(date.year), ''))

        logger.debug(' _get_news_links_by_date - Constructed URL: %s' % url)

        links_list = []

        try:
            data = urllib.request.urlopen(url)

            soup = BeautifulSoup(data)

            # 'bezformata.ru/listnews/[^"]':
            # Fetch links to news articles only
            # Exclude main link by ^"

            for link in soup.find_all('a', attrs={'href': re.compile(main_hostname + news_page_path + '[^"]')}):

                # Some links are duplicated (href for picture and new's title
                if link.get('href') not in links_list:
                    links_list.append(link.get('href'))

            logger.debug(' _get_news_links_by_date - Fetched links to pages: ' + str(links_list))

        except urllib.error.URLError as e:
            print(e.reason)

        logger.debug(' _get_news_links_by_date - OUT')

        return links_list

    def _get_news_article(self, crawler_type, crawler_name, region, link, category='Unknown'):
        """ Создает объект новости из входных данных и данных, полученных из страницы источника
        :param crawler_type:
        :param crawler_name:
        :param region:
        :param link:
        :return: NewsArticle
        """

        news = NewsArticle()
        news.crawler_type = crawler_type
        news.crawler_name = crawler_name
        news.region = region
        news.category = category
        news.url = link

        logger.debug('_get_news_article: for URL {0}'.format(link))

        try:
            article_data = urllib.request.urlopen(link)

            article_soup = BeautifulSoup(article_data)

            try:
                # Убрать текст картинок и ссылки в конце
                all_p_tag = article_soup.find('div', attrs={'id': 'hc'}).find_all('p')

                # TODO to remove CRLF
                news.text = ' '.join(''.join([tag_str.text for tag_str in all_p_tag]).split())
                news.text = '.'.join(news.text.split(';'))
                news.text = ' '.join(news.text.split('"'))
                news.text = ' '.join(news.text.split("'"))

                news.source = article_soup.find('div', attrs={'class': 'sourcelink_box'}).find('div').find(
                    'a').get_text()

                # TODO to remove CRLF
                news.title = ' '.join(article_soup.find('h1').get_text().split())
                news.title = '.'.join(news.title.split(';'))

                news.fetch_date = datetime.date.today()
                news.calc_text_md5()

                # Дата и время загрузки новости
                news.date = article_soup.find('div', attrs={'class': 'sourcedatelink_box'}).find('span').get_text()

                logger.debug('_get_news_article: fetched news: {0}'.format(news))
                logger.debug('_get_news_article: news fetched. Title is {0}'.format(news.title))
            except:
                logger.warning("_get_news_article: Can't find tag in news HTML for URL {0}".format(link))
                return None

        except urllib.error.URLError as e:
            logger.warning('_get_news_article: URL error {0} for URL {1}'.format(e.reason, link))
            news = None

        return news

    def _wait_after_news_fetching(self):
        time.sleep(self._query_timeout)


class NewsArticle():
    """ Новость: Регион, Дата новости, Источник, Категория, Заголовок, Текст (FT 1). Дополнительно имя и тип краулера.
    """

    fields_list = ['_region', '_category', '_date', '_fetch_date', '_url', '_title', '_source', '_crawler_type',
                   '_crawler_name', '_text', '_text_md5']

    def __init__(self):
        # FT 1    Нужны следующие поля по каждой новости: Регион, Дата новости, Источник, Категория, Заголовок, Текст
        self._crawler_type = None
        self._crawler_name = None
        self._region = None
        self._date = None
        self._source = None
        self._category = None
        self._title = ""
        self._text = ""
        self._text_md5 = ""
        self._url = ""
        self._fetch_date = None  # Когда подгрузили новость

    def __str__(self):
        return 'crawler type: {0}, crawler name: {1}\n' \
               'region: {2}\n' \
               'date: {3}\n' \
               'source: {4}\n' \
               'category: {5}\n' \
               'title: {6}\n' \
               'text (the beginning only): {7}\n'.format(self._crawler_type, self._crawler_name,
                                                         self._region, self._date,
                                                         self._source, self._category,
                                                         self._title, self._text[0:50])

    @property
    def crawler_type(self):
        return self._crawler_type

    @crawler_type.setter
    def crawler_type(self, value):
        self._crawler_type = value

    @property
    def crawler_name(self):
        return self._crawler_name

    @crawler_name.setter
    def crawler_name(self, value):
        self._crawler_name = value

    @property
    def region(self):
        return self._region

    @region.setter
    def region(self, value):
        self._region = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        self._source = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    @property
    def text_md5(self):
        return self._text_md5

    def calc_text_md5(self):
        m = hashlib.md5()
        m.update(self._text.encode('utf-8'))
        # TODO Fix this (possibly digest value break file output
        # self._text_md5 = m.digest()
        self._text_md5 = 'TBD'
        logger.debug("NewsArticle hash.setter: hash {0} calculated for {1}".format(self._text_md5, self._text))
        # logger.info("NewsArticle hash.setter: hash calculated")

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def fetch_date(self):
        return self._fetch_date

    @fetch_date.setter
    def fetch_date(self, value):
        self._fetch_date = value


class FileWriter():
    """ writer to csv file
    """

    # TODO filename and dirname has to be in the signature
    def __init__(self, work_folder=os.getcwd(), file_type='csv'):
        self.__header = []
        self.__delimiter = ';'
        self.__encoding = 'utf-8'

        if file_type == 'csv':
            self.file_name_suffix = 'csv'
        else:
            self.file_name_suffix = 'txt'

        self.__work_folder = work_folder

    def write_news_list(self, file_name, news_list):
        """

        :param file_name:
        :param news_list:
        :return:
        """
        file_path = os.path.abspath(self.__work_folder + '\\' + file_name + '.' + self.file_name_suffix)

        # TODO Let's try binary mode, like in examples
        with open(file_path, 'a', newline='', encoding=self.__encoding) as csvfile:
            filewriter = csv.writer(csvfile, delimiter=';', dialect='excel')

            # Fetch headers from static property of class MewsArticle as list
            items_header = NewsArticle.fields_list

            filewriter.writerow(items_header)

            for item_row in news_list:
                items_str = []
                for key in items_header:
                    items_str.append(item_row.__dict__[key])

                filewriter.writerow(items_str)
                # print(items_str)
