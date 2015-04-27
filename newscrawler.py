__author__ = 'Skimmerzzz'

import logging
import datetime

logger = logging.getLogger(__name__)

_REGIONS_BY_OKTMO_DIC = {'79': 'Республика Адыгея',
                         '84': 'Республика Алтай',
                         '80': 'Республика Башкортостан',
                         '81': 'Республика Бурятия',
                         '82': 'Республика Дагестан',
                         '26': 'Республика Ингушетия',
                         '83': 'Кабардино-Балкарская республика',
                         '85': 'Республика Калмыкия',
                         '91': 'Карачаево-Черкесская республика',
                         '86': 'Республика Карелия',
                         '87': 'Республика Коми',
                         '35': 'Республика Крым',
                         '88': 'Республика Марий Эл',
                         '89': 'Республика Мордовия',
                         '98': 'Республика Саха (Якутия)',
                         '90': 'Республика Северная Осетия — Алания',
                         '92': 'Республика Татарстан',
                         '93': 'Республика Тыва',
                         '94': 'Удмуртская республика',
                         '95': 'Республика Хакасия',
                         '96': 'Чеченская республика',
                         '97': 'Чувашская республика',
                         '1': 'Алтайский край',
                         '76': 'Забайкальский край',
                         '30': 'Камчатский край',
                         '3': 'Краснодарский край',
                         '4': 'Красноярский край',
                         '57': 'Пермский край',
                         '5': 'Приморский край',
                         '7': 'Ставропольский край',
                         '8': 'Хабаровский край',
                         '10': 'Амурская область',
                         '11': 'Архангельская область',
                         '12': 'Астраханская область',
                         '14': 'Белгородская область',
                         '15': 'Брянская область',
                         '17': 'Владимирская область',
                         '18': 'Волгоградская область',
                         '19': 'Вологодская область',
                         '20': 'Воронежская область',
                         '24': 'Ивановская область',
                         '25': 'Иркутская область',
                         '27': 'Калининградская область',
                         '29': 'Калужская область',
                         '32': 'Кемеровская область',
                         '33': 'Кировская область',
                         '34': 'Костромская область',
                         '37': 'Курганская область',
                         '38': 'Курская область',
                         '41': 'Ленинградская область',
                         '42': 'Липецкая область',
                         '44': 'Магаданская область',
                         '46': 'Московская область',
                         '47': 'Мурманская область',
                         '22': 'Нижегородская область',
                         '49': 'Новгородская область',
                         '50': 'Новосибирская область',
                         '52': 'Омская область',
                         '53': 'Оренбургская область',
                         '54': 'Орловская область',
                         '56': 'Пензенская область',
                         '58': 'Псковская область',
                         '60': 'Ростовская область',
                         '61': 'Рязанская область',
                         '36': 'Самарская область',
                         '63': 'Саратовская область',
                         '64': 'Сахалинская область',
                         '65': 'Свердловская область',
                         '66': 'Смоленская область',
                         '68': 'Тамбовская область',
                         '28': 'Тверская область',
                         '69': 'Томская область',
                         '70': 'Тульская область',
                         '71': 'Тюменская область',
                         '73': 'Ульяновская область',
                         '75': 'Челябинская область',
                         '78': 'Ярославская область',
                         '45': 'Москва',
                         '40': 'Санкт-Петербург',
                         '67': 'Севастополь',
                         '99': 'Еврейская автономная область',
                         '11-8': 'Ненецкий автономный округ',
                         '71-8': 'Ханты-Мансийский автономный округ - Югра',
                         '77': 'Чукотский автономный округ',
                         '71-9': 'Ямало-Ненецкий автономный округ'}


def get_region_name_by_oktmo(oktmo_code):
    """

    :param oktmo_code:
    :return:
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
        self._crawler_type = 'archive'

        self._start_date = datetime.date(1999, 1, 1)
        self._end_date = datetime.date.today()
        self._query_timeout = 5

        logger.debug("Archive crawler created")

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

    # TODO Insert all regions here
    _ALL_REGIONS = {'barnaul':	'1',
                    'blagoveshensk':	'10',
                    'arhangelsk':	'11',
                    'astrahan':	'12',
                    'belgorod':	'14',
                    'bryansk':	'15',
                    'vladimir':	'17',
                    'volgograd':	'18',
                    'vologda':	'19',
                    'voronej':	'20',
                    'moskva':	'45',
                    'sanktpeterburg':	'40',
                    'sevastopol':	'67',
                    'birobidjan':	'99',
                    'chita':	'76',
                    'ivanovo':	'24',
                    'irkutsk':	'25',
                    'nalchik':	'83',
                    'kaliningrad':	'27',
                    'kaluga':	'29',
                    'petropavlovskkamchatskiy':	'30',
                    'kemerovo':	'32',
                    'kirov':	'33',
                    'kostroma':	'34',
                    'krasnodar':	'3',
                    'krasnoyarsk':	'4',
                    'kurgan':	'37',
                    'kursk':	'38',
                    'lenoblast':	'41',
                    'lipeck':	'42',
                    'magadan':	'44',
                    'podmoskovye':	'46',
                    'murmansk':	'47',
                    'narianmar':	'11-8',
                    'nnovgorod':	'22',
                    'velikiynovgorod':	'49',
                    'novosibirsk':	'50',
                    'omsk':	'52',
                    'orenburg':	'53',
                    'orel':	'54',
                    'penza':	'56',
                    'perm':	'57',
                    'vladivostok':	'5',
                    'pskov':	'58',
                    'maikop':	'79',
                    'gornoaltaysk':	'84',
                    'ufa':	'80',
                    'ulanude':	'81',
                    'mahachkala':	'82',
                    'magas':	'26',
                    'elista':	'85',
                    'cherkesk':	'91',
                    'petrozavodsk':	'86',
                    'siktivkar':	'87',
                    'simferopol':	'35',
                    'yoshkarola':	'88',
                    'saransk':	'89',
                    'yakutsk':	'98',
                    'vladikavkaz':	'90',
                    'kazan':	'92',
                    'kizil':	'93',
                    'abakan':	'95',
                    'rostovnadonu':	'60',
                    'ryazan':	'61',
                    'samara':	'36',
                    'saratov':	'63',
                    'ujnosahalinsk':	'64',
                    'ekaterinburg':	'65',
                    'smolensk':	'66',
                    'stavropol':	'7',
                    'tambov':	'68',
                    'tver':	'28',
                    'tomsk':	'69',
                    'tula':	'70',
                    'tumen':	'71',
                    'ijevsk':	'94',
                    'uliyanovsk':	'73',
                    'habarovsk':	'8',
                    'hantimansiysk':	'71-8',
                    'chelyabinsk':	'75',
                    'grozniy':	'96',
                    'cheboksari':	'97',
                    'anadir':	'77',
                    'salehard':	'71-9',
                    'yaroslavl':	'78'}

    def __init__(self, start_date=datetime.date.today(), end_date=datetime.date.today()):
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

        current_date = start_date
        news_list = []

        while current_date <= end_date:
            # Получаем список ссылок новостей для заданных даты и региона
            logger.info("Fetching news' links for %s region, %s date" % (get_region_name_by_oktmo(region), str(current_date)))
            news_links_list = self._get_news_links(region, current_date)

            logger.info("Fetching %d news for %s region, %s date" % (len(news_links_list), get_region_name_by_oktmo(region), str(current_date)))
            logger.debug(news_links_list)
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

        # TODO Stub here
        return []

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

        # TODO Stub here
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


class Writer():
    """ Abstract writer
    """
    pass










