#!/usr/bin/venv python3~

import requests
from bs4 import BeautifulSoup

try:
    HTML_RUSSIA = requests.get('https://tass.ru/v-strane')
    HTML_WORLD = requests.get('https://tass.ru/mezhdunarodnaya-panorama')
except requests.exceptions.MissingSchema as exc:
    print(exc)

NEWS_RUSSIA = 'span', {'class': "text_size-23pt__3EvD_ text_color-black__3q9bA text_mobile-size-18pt__2cXcY "
                                "text_align-left__1zyXV text_font-GOSTUI2__2ODBw"}
NEWS_WORLD = 'span', \
             {'class': 'metaTag_meta__IZNP3 text_size-12pt__3S9s4 text_color-grey__2IKZv text_align-left__1zyXV '
                       'text_transform-uppercase__2Xxdu text_font-GOSTUI2__2ODBw'}


class Parser:
    """
    Парсит сайт Информационного агентсва ТАСС
    Отправляет результат парсинга в get_scenario
    """

    def __init__(self, location):
        self.location = location
        self.table_news = list()

    def run_parse(self):
        """
        запускает парсинг на оснвоании локации "ru" or "world";
        :return: <list> [новость1, новость2,..]
        """
        if self.location == 'ru':
            return self.parse_news(html=HTML_RUSSIA.text, news_local=NEWS_RUSSIA)
        elif self.location == 'world':
            return self.parse_news(html=HTML_WORLD.text, news_local=NEWS_WORLD)

    def parse_news(self, html, news_local):
        """
        :param html: BeautifulSoup obj
        :param news_local: 'ru' or 'world'
        :return: <list> [новость1, новость2,..]
        Парсинг сайтов;
        """
        soup = BeautifulSoup(html, 'html.parser')
        news = soup.findAll(news_local)
        news = list(set(news))
        if len(news) > 30:
            news = news[:(30 - len(news))]
        return [news_.text for index, news_ in enumerate(news) if 20 < len(news_.text) < 130]
