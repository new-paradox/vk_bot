#!/usr/bin/venv python3~
import re
from operator import itemgetter
from pprint import pprint

import requests
from bs4 import BeautifulSoup

HTML_RUSSIA = requests.get('https://tass.ru/v-strane').text
HTML_WORLD = requests.get('https://tass.ru/mezhdunarodnaya-panorama').text


class Handler:
    def __init__(self, location):
        self.location = location
        self.table_news = list()

    def run_parse(self):
        if self.location == 'ru':
            return self.parse_ru_news()
        elif self.location == 'world':
            return self.parse_world_news()

    def parse_ru_news(self):
        soup = BeautifulSoup(HTML_RUSSIA, 'html.parser')
        time = soup.findAll('div', {'class': 'flex_base__1iNR3 flex_direction_row__3mAza'})
        news = soup.findAll('span',
                            {'class': "text_size-23pt__3EvD_ text_color-black__3q9bA text_mobile-size-18pt__2cXcY "
                                      "text_align-left__1zyXV text_font-GOSTUI2__2ODBw"})
        print(news)
        print(time)
        time = list(set(time[(len(time) - len(news)):]))
        news = list(set(news))
        for index, elem_news in enumerate(news):
            news_now = elem_news.text
            news_time = time[index].text
            self.table_news.append((news_time, news_now))
        return sorted(self.table_news, key=itemgetter(0), reverse=False)

    def parse_world_news(self):
        soup = BeautifulSoup(HTML_WORLD, 'html.parser')
        time = soup.findAll('div', {'class': 'flex_base__1iNR3 flex_direction_row__3mAza'})
        news = soup.findAll('span',
                            {'class': "text_size-23pt__3EvD_ text_color-black__3q9bA text_mobile-size-18pt__2cXcY "
                                      "text_align-left__1zyXV text_font-GOSTUI2__2ODBw"})
        print(news)
        print(time)
        time = list(set(time[(len(time) - len(news)):]))
        news = list(set(news))
        for index, elem_news in enumerate(news):
            news_now = elem_news.text
            news_time = time[index].text
            self.table_news.append((news_time, news_now))
        return sorted(self.table_news, key=itemgetter(0), reverse=False)


if __name__ == '__main__':
    Handler('ru').run_parse()
    pass

# class Handler:
#     def __init__(self, location):
#         self.location = location
#
#     def run_parse(self):
#         if self.location == 'ru':
#             return self.parse_ru_news()
#         elif self.location == 'world':
#             return self.parse_world_news()
#
#     def parse_ru_news(self):
#         news = list()
#         news.append('В иркутске все окей')
#         news.append('люди бегут из Иркутска')
#         return news
#
#     def parse_world_news(self):
#         news = list()
#         news.append('В мире все окей')
#         news.append('война в армении')
#         return news
