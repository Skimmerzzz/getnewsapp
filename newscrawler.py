__author__ = 'Skimmerzzz'

import logging
import datetime

logger = logging.getLogger(__name__)


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
    ALL_REGIONS = {'Москва': 'moskva'}

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
            logger.info("Fetching news' links for %s region, %s date" % (region, str(current_date)))
            news_links_list = self._get_news_links(region, current_date)

            logger.info("Fetching %d news for %s region, %s date" % (len(news_links_list), region, str(current_date)))
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










