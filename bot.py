#!/usr/bin/venv python3~
# -*- coding: utf-8 -*-
import requests
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from Parsers import Parser
from connect_db import Connect


class Bot:
    """
    Bot for VK API
    use python3.8

    Бот всегда слушает, когда поступает сообщение
    от пользователя, пользователь заносится в users;
    Бот начинает обрабатывать событие - on_event, если событие в сценарии - сценарий начинает
    работать - get_scenario;
    сценарий содержит в себе варианты запуска парсера сайта информмционного агентсва ТАСС
    по соответсвующим критериям (новости России или мира), полученный ответ возвращается пользователю -
    message_send;

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
        self.users = dict()

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
        обработка поступающих сообщений;
        Если это тектовое сообщение -> начинается его обработка
        Если пользователя нет в users, бот здоровается с пользователем;
        И добавляет его в users;
        Если пользователь уже есть в users -> начинается отработка сценария;
        Распаковка полученного запроса из db;
        Если сообщение от пользователя подходит по ключам к сцению -> запускается
        соотвествующий сценарий;
        Иначе пользователь получает default_answer.
        """
        if event.type == VkBotEventType.MESSAGE_NEW:
            user_id = event.object.message['from_id']
            text = event.object.message['text'].lower()

            # запрос из бд
            scenarios, intents, default_answer = Connect().connect_to_db()
            print(text)
            # приветствие
            if user_id not in self.users:
                self.users[user_id] = user_id
                self.message_send(text_to_send=intents[0]['answer'], user_id=user_id)
            else:  # сценарий
                for intent in intents:

                    if text in intent['tokens'].lower():
                        print('есть нужный ответ')
                        text_to_send = self.get_scenario(scenario_name=intent['scenario'], scenarios=scenarios)
                        self.message_send(text_to_send=text_to_send, user_id=user_id)
                        break
                else:
                    self.message_send(text_to_send=default_answer['text'], user_id=user_id)

    def message_send(self, text_to_send, user_id):
        """
        :param text_to_send: <str> ответ пользователю
        :param user_id: id пользователя в вк
        Отправка ответа пользователю;
        """
        self.api.messages.send(
            message=text_to_send,
            random_id=0,
            user_id=user_id)

    def get_scenario(self, scenario_name, scenarios):
        """
        :param scenarios:
        :param scenario_name: <str> "ru" or "world"
        :return: <str> ответ пользователю
        Обработка сценария;
        Парсинг сайтов - Parser;
        """
        for scenario in scenarios:
            if scenario_name == scenario['name']:
                break
        try:
            text_to_send = scenario['text']
            for news in Parser(location=scenario_name).run_parse():
                text_to_send += f'\n- {news}\n'
            return text_to_send
        except requests.exceptions.MissingSchema:
            return scenario['failure_parse']
