#!/usr/bin/venv python3~
import re
# import


class Handler:
    def __init__(self, location):
        self.location = location

    def run_parse(self):
        if self.location == 'ru':
            return self.parse_ru_news()
        elif self.location == 'world':
            return self.parse_world_news()

    def parse_ru_news(self):
        news = list()
        news.append('В иркутске все окей')
        news.append('Выпал снег')
        return news

    def parse_world_news(self):
        news = list()
        news.append('В мире все окей')
        news.append('Опять войны')
        return news


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
