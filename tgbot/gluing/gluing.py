from tgbot.service import get_test, get_answer, get_question, get_count, get_check_admission, send_result
from tgbot.keyboard import test_button, go_test_button, answer_button_type_one, answer_button_type_two_1, \
    answer_button_type_four, answer_button_type_two_2
from tgbot.database import check_user, add_user, del_user, add_test_id, get_id_test, check_answer, add_answer, \
    dict_answer, add_answer_type_two, get_id_user, del_user_by_peer_id
from config import LIST_TEST, ERROR, END


async def check_info_user(contact, user_id):
    '''
        Проверяет наличие записи о пользователе в таблице БД.
                Параметры:
                        contact (str): номер телефона.
                        user_id (int): id пользователя telegram.
        '''
    if check_user(get_check_admission(str(contact))['Id']):
        add_user(get_check_admission(str(contact))['Id'], user_id)  # Если нет записи о пользователе, то создаём новую
    else:
        del_user(get_check_admission(str(contact))['Id'])  # Если есть, то удаляем и создаём новую
        add_user(get_check_admission(str(contact))['Id'], user_id)
    return


async def access_verification(contact, user_id):
    '''
        Проверяет доступ к тестам.
                Параметры:
                        contact (str): номер телефона.
                        user_id (int): id пользователя telegram.
                Возвращаемое значение:
                        (str): текст сообщения and (set) кнопки с названиями тестов.
        '''
    contact = contact if '+' in contact else "+" + contact
    await check_info_user(contact, user_id)
    if get_check_admission(str(contact)) == 0:
        return f"<b>{ERROR}</b>", None
    else:
        return f"<b>{LIST_TEST}</b>", test_button(str(contact))


async def information_test(id_test):
    '''
        Возвращяет информацию о тесте.
                Параметры:
                        id_test (str): id теста.
                Возвращаемое значение:
                        (str): текст сообщения and (set) кнопка "Начать".
        '''
    return f"<b>Название:</b> {str(get_test(int(id_test))['Name'])} \n<b>Описание:</b> {str(get_test(int(id_test))['Description'])} \n<b>Количество вопросов:</b> {str(get_count(int(id_test)))}", go_test_button(
        id_test)


async def add_id_test(user_id, id_test):
    '''
        Добовляет id выполняемого теста в таблицу БД.
                Параметры:
                        user_id (int): id пользователя telegram.
                        id_test (str): id теста.
        '''
    add_test_id(user_id, id_test)


async def send_question(number, user_id):
    '''
        Проверяет номер вопроса, тип. Возвращяет текст сообщения и кнопки
                Параметры:
                        number (int): номер вопроса.
                        user_id (int): id пользователя telegram.

        '''
    # Проверка превышает ли номер вопроса кол-во их в тесте, если да, то завершаем выполнение теста, если нет то проверяем тип вопроса.
    if number <= get_count(get_id_test(user_id)):
        question_type = get_question(get_id_test(user_id), number)['Question_type']
        if question_type == 1:  # Если тип вопроса 1, возвращяем текст сообщения, и  кнопки с ответами.

        elif question_type == 2:  # Если тип вопроса 2, проверяем были ли другие ответы на этот вопрос.

        elif question_type == 3:  # Если тип вопроса 3 возвращяем текст вопроса без кнопок.

        else:  # Если тип вопроса 4 возвращяем текст вопроса и кнопки

    else:
        if send_result(get_id_user(user_id), get_id_test(user_id), dict_answer(user_id)) == 200:
            del_user_by_peer_id(id_tg=user_id)
            return f"<b>{END}</b>", 'end'
        else:
            del_user_by_peer_id(id_tg=user_id)
            return f"<b>{ERROR}</b>", 'end'


async def set_answer(user_id, data):
    '''
        Добавляет ответ в таблицу БД
                Параметры:
                        user_id (int): id пользователя telegram.
                        data (str): ответ пользователя.
                Возвращаемое значение:
                        (int): кол-во ответов в таблице БД.
        '''
    if check_answer(user_id):  # Если ответы уже есть, извлекаем их как словарь, и добавляем ответ в конец, далее записываем обратно в таблицу.
        for answ in get_answer(int(data.split('|')[0])):
            if answ["Answer_num"] == int(data.split('|')[1]):
                return add_answer(dict_answer(user_id), user_id, data.split('|')[2], answ["Answer"])
    else:  # Если нет то создаём новый словарь.
        for answ in get_answer(int(data.split('|')[0])):
            if answ["Answer_num"] == int(data.split('|')[1]):
                return add_answer(dict(), user_id, data.split('|')[2], answ["Answer"])


async def set_answer_type_two(user_id, data):
    '''
        Добавляет ответ в таблицу БД
                Параметры:
                        user_id (int): id пользователя telegram.
                        data (str): ответ пользователя.
                Возвращаемое значение:
                        (int): кол-во ответов в таблице БД.
        '''
    if check_answer(
            user_id):  # Если ответы уже есть, извлекаем их как словарь, и добавляем ответ в конец, далее записываем обратно в таблицу.
        for answ in get_answer(int(data.split('|')[0])):
            if answ["Answer_num"] == int(data.split('|')[1]):
                if str(data.split('|')[2]) in dict_answer(user_id):
                    return add_answer_type_two(dict_answer(user_id), str(data.split('|')[2]),
                                               str(len(dict_answer(user_id)[str(data.split('|')[2])]) + 1), user_id,
                                               answ["Answer"])
                else:
                    return add_answer(dict_answer(user_id), user_id, data.split('|')[2], {'1': answ["Answer"]})
    else:  # Если нет то создаём новый словарь.
        for answ in get_answer(int(data.split('|')[0])):
            if answ["Answer_num"] == int(data.split('|')[1]):
                return add_answer(dict_answer(user_id), user_id, data.split('|')[2], {'1': answ["Answer"]})


async def set_answer_type_three(user_id, data):
    '''
        Добавляет ответ в таблицу БД
                Параметры:
                        user_id (int): id пользователя telegram.
                        data (str): ответ пользователя.
                Возвращаемое значение:
                        (int): кол-во ответов в таблице БД.
        '''
    if check_answer(user_id):  # Если ответы уже есть, извлекаем их как словарь, и добавляем ответ в конец, далее записываем обратно в таблицу.
        return add_answer(dict_answer(user_id), user_id, len(dict_answer(user_id)) + 1, data)
    else:  # Если нет то создаём новый словарь.
        return add_answer(dict(), user_id, 1, data)
