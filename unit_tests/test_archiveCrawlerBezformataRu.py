from unittest import TestCase
import newscrawler

__author__ = 'Computer'


class TestArchiveCrawlerBezformataRu(TestCase):
  def test_get_news_links_number(self):

      cr = newscrawler.ArchiveCrawlerBezformataRu()
      news_num = cr.get_news_links_number('41', 'finance')

      # We have 65 links to news for 41 region and finance category
      self.assertEqual(news_num, 65)
      #self.fail()
