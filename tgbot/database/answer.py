from tgbot.database.database import engine, Answer
from sqlalchemy.orm import sessionmaker

DBSession = sessionmaker(bind=engine)
session = DBSession()


def add_user(id_user, id_tg):
    '''
        Добавляет id пользователя из системы ВУЗа и telegram в таблицу БД.
                Параметры:
                        id_user (str): id пользователя.
                        id_tg (str): id пользователя telegram.
        '''
    session.add(Answer(id_user, id_tg, None, None))
    session.commit()


def del_user(id_user):
    '''
        Удаляет информацию о пользователе из таблицы БД по вузовскому id.
                Параметры:
                        id_user (str): id пользователя из системы ВУЗа.
        '''
    session.delete(session.query(Answer).filter_by(id_user=id_user).one())
    session.commit()


def del_user_by_peer_id(id_tg):
    '''
        Удаляет информацию о пользователе из таблицы БД по телеграмм id.
                Параметры:
                        id_tg (str): id пользователя telegram.
        '''
    session.delete(session.query(Answer).filter_by(id_tg=id_tg).one())
    session.commit()


def check_user(id_user):
    '''
        Проверяет есть ли запись о пользователе в таблице БД.
                Параметры:
                        id_user (str): id пользователя telegram.
                Возвращаемое значение:
                        True or False.
        '''
    if session.query(Answer).filter(Answer.id_user == id_user).first() != None:
        return False
    else:

        return True


def add_test_id(id_user, id_test):
    '''
        Добавляет id теста к пользователю в таблицу БД.
                Параметры:
                        user_id (str): id пользователя telegram.
                        id_test (str): id теста.
        '''
    i = session.query(Answer).get(id_user)
    i.id_test = id_test
    session.add(i)
    session.commit()


def get_id_test(user_id):
    '''
        Возвращяет id теста из таблицы БД.
                Параметры:
                        user_id (str): id пользователя telegram.
                Возвращаемое значение:
                        (int): id теста.
        '''
    return int(session.query(Answer).get(user_id).id_test)


def get_id_user(user_id):
    '''
        Возвращяет id пользователя из таблицы БД.
                Параметры:
                        user_id (str): id пользователя telegram.
                Возвращаемое значение:
                        (int): id пользователя.
        '''
    return int(session.query(Answer).get(user_id).id_user)


def check_answer(user_id):
    '''
        Проверяет есть ли ответы пользователя в таблице БД.
                Параметры:
                        user_id (str): id пользователя telegram.
                Возвращаемое значение:
                        True or False.
        '''
    if session.query(Answer).get(user_id).answer != None:
        return True
    else:
        return False


def add_answer(dict_answer, user_id, number, answer):
    '''
            Добавляет ответы на вопросы типов: 1,3,4 в таблицу БД.
                    Параметры:
                            dict_answer (dict): словарь с ответами.
                            user_id (str): id пользователя telegram.
                            number (int): номер вопроса.
                            answer (str): ответ.
                    Возвращаемое значение:
                            (int): размер словаря с ответами.
            '''
    dict_answer[number] = answer
    i = session.query(Answer).get(user_id)
    i.answer = str(dict_answer)
    session.add(i)
    session.commit()
    return len(dict_answer)


def add_answer_type_two(dict_answer, num_1, num_2, user_id, answer):
    '''
            Добавляет ответы на вопросы типа 2 в таблицу БД.
                    Параметры:
                            dict_answer (dict): словарь с ответами.
                            num_1 (str): номер вопроса.
                            num_2 (int): номер варианта отаета на этот вопрос.
                            user_id (str): id пользователя telegram.
                            answer (str): ответ.
                    Возвращаемое значение:
                            (int): размер словаря с ответами.
            '''
    dict_answer[num_1][num_2] = answer
    i = session.query(Answer).get(user_id)
    i.answer = str(dict_answer)
    session.add(i)
    session.commit()
    return len(dict_answer)


def dict_answer(user_id):
    '''
            Возвращяет ответы из таблицы в виде словаря.
                    Параметры:
                            user_id (str): id пользователя telegram.
                    Возвращаемое значение:
                            (dict): словарь с ответами.
            '''
    return eval(str(session.query(Answer).get(user_id).answer))
