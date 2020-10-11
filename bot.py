#!/usr/bin/venv python3~
# -*- coding: utf-8 -*-

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import time
import logging
from random import randint

try:
    import config
except ImportError:
    exit('DO cp config.py.default config.py and set token')

log = logging.getLogger('bot')


def configure_logging():
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
    stream_handler.setLevel(logging.INFO)
    log.addHandler(stream_handler)

    file_handler = logging.FileHandler('bot.log', encoding='utf-8')
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s, %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
    file_handler.setLevel(logging.DEBUG)
    log.addHandler(file_handler)

    log.setLevel(logging.DEBUG)


class Bot:
    """
    echo bot for VK API
    use python3.8
    """

    def __init__(self, id_group, token_):
        """
        :param id_group: group id из vk
        :param token_: секретный токен
        """
        self.id_group = id_group
        self.vk = vk_api.VkApi(token=token_)
        self.long_poller = VkBotLongPoll(self.vk, self.id_group)
        self.api = self.vk.get_api()

    def run(self):
        """
        Запуск бота
        """
        for event in self.long_poller.listen():
            """
            :param event: VkBotMessageEvent obj
            :return: None
            """
            try:
                self.on_event(event)
            except Exception:
                log.exception('ошибка в обработке события')

    def on_event(self, event):
        """
        обработка сообщений
        """
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.object.message['text']:
                log.debug('отправляю сообщение пользователю')
                self.api.messages.send(
                    message=event.object.message['text'],
                    random_id=randint(0, 2 * 10),
                    user_id=event.object.message['from_id'])
        elif event.type == VkBotEventType.MESSAGE_TYPING_STATE:
            log.debug('пользователь набирает сообщение')
        else:
            log.info('Пока не умеем обрабатывать события типа %s', event.type)
            # raise ValueError('неизвестное сообщение')


if __name__ == '__main__':
    configure_logging()
    bot = Bot(id_group=config.GROUP_ID, token_=config.TOKEN)
    bot.run()
