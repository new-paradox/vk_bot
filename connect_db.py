from contextlib import closing
import pymysql
from pymysql.cursors import DictCursor


class Connect:
    """
    Подключение к базе данных
    """
    def connect_to_db(self):
        with closing(pymysql.connect(
                host='localhost',
                user='bot',
                password='1',
                db='vkbot',
                charset='utf8mb4',
                cursorclass=DictCursor
        )) as connection:
            scenarios = select_scenarios(connection)
            intents = select_intents(connection)
            default_answer = select_default_answer(connection)
            return scenarios, intents, default_answer


def select_scenarios(connection):
    """
    Запрос сценария
    """
    scenarios = list()
    with connection.cursor() as cursor:
        query = """
        SELECT name, text, failure_parse  FROM scenarios
        """
        cursor.execute(query)
        for row in cursor:
            scenarios.append(row)
        return scenarios


def select_intents(connection):
    """
    Запрос ключевых слов
    """
    intents = list()
    with connection.cursor() as cursor:
        query = """
        SELECT name, tokens, scenario, answer FROM intents
        """
        cursor.execute(query)
        for row in cursor:
            intents.append(row)
        return intents


def select_default_answer(connection):
    """
    Запрос ответа по умолчанию
    """
    default_answer = None
    with connection.cursor() as cursor:
        query = """
        SELECT text FROM default_answer WHERE id = 1
        """
        cursor.execute(query)
        for row in cursor:
            default_answer = row
        return default_answer
