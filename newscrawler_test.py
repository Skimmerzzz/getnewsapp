__author__ = 'Skimmerzzz'

import unittest
import newscrawler
import datetime


class MyTestCase(unittest.TestCase):
    def setUp(self):
        # Test online article
        self.__article_url = 'http://moskva.bezformata.ru/listnews/himkah-muzhchina-otnyal-u-politcejskogo/32405548/'
        self.__article_text = 'Полицейский в Химках расстрелял мужчину, который отнял у его напарника пистолет ' \
                              'и открыл беспорядочную стрельбу, сообщили в пресс-службе областного главка МВД.' \
                              ' По данным АГН "Москва" , инцидент произошел накануне в подмосковных Химках. ' \
                              'Полицейские приехали в один из домов по вызову о семейной ссоре. В ходе задержания ' \
                              '32-летний мужчина оказал сопротивление стражам порядка, выхватил у одного из них' \
                              ' пистолет и открыл беспорядочную стрельбу. Второй сотрудник полиции в соответствии' \
                              ' с законом "О полиции" произвел предупредительный выстрел вверх, а затем выстрелил ' \
                              'в злоумышленника и ранил его. Мужчину госпитализировали с ранениями различной ' \
                              'степени тяжести. В настоящее время по данному факту проводится служебная проверка.'

        self.__article_title = 'В Химках мужчина отнял у полицейского пистолет и открыл стрельбу'

        self.__start_date = datetime.date(2015, 4, 20)
        self.__end_date = datetime.date(2015, 4, 20)

        self.__bzfrmt = newscrawler.ArchiveCrawlerBezformataRu()
        self.__news = self.__bzfrmt._get_news_article('archive', 'BezformataRu', '45', self.__article_url)
        self.__news_by_category = self.__bzfrmt._get_news_article('archive', 'BezformataRu', '45', self.__article_url, category='finance')
        self.__news_as_str = 'crawler type: archive, crawler name: BezformataRu\n' \
            'region: 45\n'\
            'date: 29.04.2015  19:26\n'\
            'source: Molnet.Ru\n'\
            'category: finance\n'\
            'title: В Химках мужчина отнял у полицейского пистолет и открыл стрельбу\n'\
            'text (the beginning only): Полицейский в Химках расстрелял мужчину, который о\n'\

    def test_get_news_article(self):

        self.assertEqual(self.__news.title, self.__article_title)
        self.assertEqual(self.__news.text, self.__article_text)

        news_as_str = 'crawler type: archive, crawler name: BezformataRu\n' \
            'region: 45\n'\
            'date: 29.04.2015  19:26\n'\
            'source: Molnet.Ru\n'\
            'category: Unknown\n'\
            'title: В Химках мужчина отнял у полицейского пистолет и открыл стрельбу\n'\
            'text (the beginning only): Полицейский в Химках расстрелял мужчину, который о\n'\

        self.assertEqual(str(self.__news), news_as_str)

    def test_get_news_article_with_category(self):
        self.assertEqual(True, True)

    """def test_get_news_by_category_n_page(self):

        news_list = self.__bzfrmt.get_news_by_category_n_page('45', 'finance', 1, 1)
        self.assertListEqual(news_list, [self.__news_by_category])
    """

    def test_get_news_links_by_page(self):

        news_url_list = self.__bzfrmt._get_news_links_by_page('45', 'finance', 1)
        self.assertListEqual(news_url_list, [self.__article_url])


    #def test_csvwriter_write(self):
    #    cw = newscrawler.FileWriter()
    #    cw.write(self.__news)


if __name__ == '__main__':
    unittest.main()
