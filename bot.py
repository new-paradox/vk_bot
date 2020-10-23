#!/usr/bin/venv python3~
# -*- coding: utf-8 -*-

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from Parsers import Parser

try:
    import config
except ImportError:
    exit('DO cp config.py.default config.py and set token')


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
        self.user_states = dict()

    def run(self):
        """
        Запуск бота
        """
        for event in self.long_poller.listen():
            """
            :param event: VkBotMessageEvent obj
            :return: None
            """
            self.on_event(event)

    def on_event(self, event):
        """
        обработка сообщений
        """
        if event.type == VkBotEventType.MESSAGE_NEW:
            user_id = event.object.message['from_id']
            text = event.object.message['text'].lower()
            print(text)

            if user_id not in self.user_states:
                # приветствую нового пользователя
                self.user_states[user_id] = user_id
                self.message_send(text_to_send=config.INTENTS[0]['answer'], user_id=user_id)
            else:
                # обработка сценария
                for intent in config.INTENTS:
                    if text in intent['tokens']:
                        print('есть нужный ответ')  # TODO: добавить логирование
                        print(intent['scenario'])   #  добавить обработку 400-500
                        text_to_send = self.start_scenario(scenario_name=intent['scenario'])
                        self.message_send(text_to_send=text_to_send, user_id=user_id)
                        break
                else:
                    self.message_send(text_to_send=config.DEFAULT_ANSWER, user_id=user_id)

    def message_send(self, text_to_send, user_id):
        self.api.messages.send(
            message=text_to_send,
            random_id=0,
            user_id=user_id)

    def start_scenario(self, scenario_name):
        scenario = config.SCENARIOS[scenario_name]
        text_to_send = scenario['text']
        for time, news in Parser(location=scenario_name).run_parse():
            text_to_send += f'\n{time} - {news}\n'
        return text_to_send


if __name__ == '__main__':
    bot = Bot(id_group=config.GROUP_ID, token_=config.TOKEN)
    bot.run()
