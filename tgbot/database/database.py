from sqlalchemy import create_engine, Table, Integer, Column, Text, URL
from sqlalchemy.orm import registry

from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, DB_ENGINE

'''
Подключение к БД и создание класса таблицы "answer_user".
'''
url = URL.create(
    DB_ENGINE,
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)
engine = create_engine(url)
engine.connect()

mapper_registry = registry()

answers = Table("answer_user", mapper_registry.metadata,
                Column("id_user", Integer()),
                Column("id_tg", Integer(), primary_key=True),
                Column("id_test", Integer()),
                Column("answer", Text()))


class Answer():
    def __init__(self, id_user, id_tg, id_test, answer):
        self.id_user = id_user
        self.id_tg = id_tg
        self.id_test = id_test
        self.answer = answer


mapper_registry.map_imperatively(Answer, answers)
mapper_registry.metadata.create_all(engine)
