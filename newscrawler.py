__author__ = 'Skimmerzzz'

import logging
import datetime
import urllib.request
import urllib.error
import re
import urllib.parse
import os
import sys
import csv

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

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
        self._query_timeout = 5

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

    def __init__(self, start_date=datetime.date.today(), end_date=datetime.date.today()):

        ArchiveCrawler.__init__(self)
        self._crawler_name = 'BezformataRu'
        self._start_date = start_date
        self._end_date = end_date

    # TODO Make dates optional
    def get_region_news(self, region, start_date, end_date):
        """ Получить новости региона в заданном диапазоне дат.
        :param region: Регион, для которого получаем новости
        :param start_date:
        :param end_date:
        :return: Список объектов новостей NewsArticle
        """

        logger.debug(' get_region_news - IN')

        current_date = start_date
        news_list = []

        while current_date <= end_date:
            # Получаем список ссылок новостей для заданных даты и региона
            logger.info("Fetching news' links for %s region, %s date" % (
                get_region_name_by_oktmo(region)[0], str(current_date)))

            news_links_list = self._get_news_links(region, current_date)

            logger.info("Fetching %d news' links to pages for %s region, %s date" % (
                len(news_links_list), get_region_name_by_oktmo(region)[0], str(current_date)))

            for link in news_links_list:
                news_article = self._get_news_article(self._crawler_type, self._crawler_name, region, link)
                if news_article is None:
                    continue
                else:
                    news_list.append(news_article)
            current_date = current_date + datetime.timedelta(days=1)

        logger.info("Fetched %d news" % len(news_list))
        logger.debug(news_list)
        return news_list

    def _get_news_links(self, region, date):
        """ Получить ссылки на новости для заданных даты и региона
        :param region: Регион
        :param date: Дата
        :return: Список ссылок на новости для заданных даты и региона
        """

        logger.debug(' _get_news_links - IN')

        main_hostname = 'bezformata.ru'
        news_links_page_path = '/daysnews/'
        news_page_path = '/listnews/'

        # Url example 'http://moskva.bezformata.ru/daynews/?nday=20&nmonth=4&nyear=2015'
        url = urllib.parse.urlunparse(('http', get_region_name_by_oktmo(region)[1] + '.' + main_hostname,
                                       news_links_page_path, '', 'nday=' + str(date.day) + '&nmonth='
                                       + str(date.month) + '&nyear=' + str(date.year), ''))

        logger.debug(' _get_news_links - Constructed URL: %s' % url)

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

            logger.debug(' _get_news_links - Fetched links to pages: ' + str(links_list))

        except urllib.error.URLError as e:
            print(e.reason)

        logger.debug(' _get_news_links - OUT')

        return links_list

    def _get_news_article(self, crawler_type, crawler_name, region, link):
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

        logger.info('_get_news_article: for URL {0}'.format(link))

        try:
            article_data = urllib.request.urlopen(link)

            article_soup = BeautifulSoup(article_data)

            # Убрать текст картинок и ссылки в конце
            all_p_tag = article_soup.find('div', attrs={'id': 'hc'}).find_all('p')
            news.text = ''.join([tag_str.text for tag_str in all_p_tag])

            news.source = article_soup.find('div', attrs={'class': 'sourcelink_box'}).find('div').find('a').get_text()

            news.title = article_soup.find('h1').get_text()

            logger.debug('_get_news_article: fetched news: {0}'.format(news))
            logger.info('_get_news_article: news fetched. Title is {0}'.format(news.title))


        except urllib.error.URLError as e:
            logger.warning('_get_news_article: URL error {0} for URL {1}'.format(e.reason, link))
            news = None

        return news

    def get_all_news(self, start_date, end_date):
        pass


class NewsArticle():
    """ Новость: Регион, Дата новости, Источник, Категория, Заголовок, Текст (FT 1). Дополнительно имя и тип краулера.
    """

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


class CsvWriter():
    """ writer to csv file
    """

    def __init__(self):
        self.__header = []
        self.__delimiter = ';'
        self.__encoding = 'utf-8'
        self.__file_name = 'out.csv'
        self.__work_folder = os.getcwd()

    def write(self, news):
        file_path = os.path.abspath(self.__work_folder + '\\' + self.__file_name)
        test = news.__dict__
        with open(file_path, 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=';')

            # TODO Rewrite this!!!

            items_str = []
            for item in news.__dict__:
                items_str.append(item)

            filewriter.writerow(items_str)

            # TODO Rewrite this!!!

            """self._crawler_type = None
            self._crawler_name = None
            self._region = None
            self._date = None
            self._source = None
            self._category = None
            self._title = ""
            self._text = ""
            """

            items_str = []
            for item in news.__dict__:
                items_str.append(news.__dict__[item])

            filewriter.writerow(items_str)

















