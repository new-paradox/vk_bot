from contextlib import closing
import pymysql
from pymysql.cursors import DictCursor


class Connect:
    def __init__(self):
        self.scenarios = list()
        self.default_answer = list()
        self.intents = list()

    def connect_to_db(self):
        with closing(pymysql.connect(
                host='localhost',
                user='bot',
                password='1',
                db='vkbot',
                charset='utf8mb4',
                cursorclass=DictCursor
        )) as connection:
            with connection.cursor() as cursor:
                query = """
                SELECT name, text, failure_parse  FROM scenarios
                """
                cursor.execute(query)
                for row in cursor:
                    self.scenarios.append(row)
            with connection.cursor() as cursor:
                query = """
                SELECT name, tokens, scenario, answer FROM intents
                """
                cursor.execute(query)
                for row in cursor:
                    self.intents.append(row)

            with connection.cursor() as cursor:
                query = """
                SELECT text FROM default_answer WHERE id = 1
                """
                cursor.execute(query)
                for row in cursor:
                    self.default_answer = row
            return self.scenarios, self.intents, self.default_answer
