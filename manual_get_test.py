__author__ = 'ssenachin'

import urllib.request
import urllib.error
import re
from bs4 import BeautifulSoup

print("GET ARTICLES LINKS")

url = 'http://moskva.bezformata.ru/daynews/?nday=20&nmonth=4&nyear=2015'

try:
    data = urllib.request.urlopen(url)
    #print(data.read(500).decode('utf-8'))

    soup = BeautifulSoup(data)

    #print(soup.prettify())


    # 'bezformata.ru/listnews/[^"]':
    # Fetch links to news articles only
    # Exclude main link by ^"
    links_list = []
    for link in soup.find_all('a', attrs={'href': re.compile('bezformata.ru/listnews/[^"]')}):
        # Some links are duplicated (href for picture and new's title
        if link.get('href') not in links_list:
            links_list.append(link.get('href'))
        #print(link.get('href'))

    print(links_list)

except urllib.error.URLError as e:
    print(e.reason)


article_url = 'http://moskva.bezformata.ru/listnews/stolichnie-developeri-menyayut-profil/31968945/'

print("GET ARTICLE TEXT")


try:
    article_data = urllib.request.urlopen(article_url)

    article_soup = BeautifulSoup(article_data)

    article_text = article_soup.find('div', attrs={'id': 'hc'}).get_text()

    print(article_text)


except urllib.error.URLError as e:
    print(e.reason)


