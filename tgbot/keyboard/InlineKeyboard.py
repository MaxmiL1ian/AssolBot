from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.service import get_check_admission, get_tests, get_test, get_answer, get_question
from config import GO_MESSAGE,NEXT_QUESTION,SELECTED

def test_button(contact):
    '''
        Возвращает объект InlineKeyboardMarkup с названиями тестов.
                Параметры:
                        contact (str): номер телефона пользователя.
                Возвращаемое значение:
                        markup_test (set): кнопки с названиями тестов.
        '''
    markup_test = InlineKeyboardMarkup()
    for i in range(len(get_tests(get_check_admission(contact)['Id']))):
         markup_test.add(
             InlineKeyboardButton(
                 text=str(get_test(get_tests(get_check_admission(contact)['Id'])[i]['Test_id'])['Name']),
                 callback_data=str('t' + str(get_test(get_tests(get_check_admission(contact)['Id'])[i]['Test_id'])['ID']))
             )
        )
    return markup_test


def go_test_button(id_test):
    '''
        Возвращает объект InlineKeyboardMarkup с кнопкой "начать".
                Параметры:
                        id_test (str): id теста.
                Возвращаемое значение:
                        markup_start (set): кнопка "начать".
        '''
    markup_start = InlineKeyboardMarkup()
    markup_start.add(InlineKeyboardButton(
        text=GO_MESSAGE, callback_data=str('g' + id_test)))
    return markup_start


def answer_button_type_one(id_test, number):
    '''
        Возвращает объект InlineKeyboardMarkup с вариантами ответов. Для вопросов типа №1.
                Параметры:
                        id_test (str): id теста.
                        number (int): номер вопроса.
                Возвращаемое значение:
                        markup_answer_type_one (set): кнопки с вариантами ответов.
        '''
    markup_answer_type_one = InlineKeyboardMarkup()
    for j in get_answer(get_question(id_test, number)['Id']):
        markup_answer_type_one.add(InlineKeyboardButton(text=str(j['Answer']), callback_data=str(
            'a' + str(j['Question_id']) + '|' + str(j['Answer_num']) + '|' + str(number))))
    return markup_answer_type_one


def answer_button_type_two_1(id_test, number):
    '''
        Возвращает объект InlineKeyboardMarkup с вариантами ответов. Для вопросов типа №2(если до этого не выбирали другие варианты ответа в этом вопросе).
                Параметры:
                        id_test (str): id теста.
                        number (int): номер вопроса.
                Возвращаемое значение:
                        markup_answer_type_two (set): кнопки с вариантами ответов.
        '''
    markup_answer_type_two = InlineKeyboardMarkup()
    for j in get_answer(get_question(id_test, number)['Id']):
        markup_answer_type_two.add(InlineKeyboardButton(text=str(j['Answer']), callback_data=str(
            'd' + str(j['Question_id']) + '|' + str(j['Answer_num']) + '|' + str(number))))
    return markup_answer_type_two


def answer_button_type_two_2(id_test, number, dict_answer):
    '''
        Возвращает объект InlineKeyboardMarkup с вариантами ответов. Для вопросов типа №2(если до этого выбирали другие варианты ответа в этом вопросе).
                Параметры:
                        id_test (str): id теста.
                        number (int): номер вопроса.
                        dict_answer (dict): словарь с ответами.
                Возвращаемое значение:
                        markup_answer_type_two (set): кнопки с вариантами ответов.
        '''
    markup_answer_type_two = InlineKeyboardMarkup()
    for j in get_answer(get_question(id_test, number)['Id']):
        if not (str(j['Answer']) in dict_answer[str(number)].values()):
            markup_answer_type_two.add(InlineKeyboardButton(text=str(j['Answer']), callback_data=str(
                'd' + str(j['Question_id']) + '|' + str(j['Answer_num']) + '|' + str(number))))
        else:
            markup_answer_type_two.add(InlineKeyboardButton(
                text=SELECTED + str(j['Answer']), callback_data='disenable'))

    if len(dict_answer[str(number)].values()) >= get_question(id_test, number)['Min_count_answer'] and len(
            dict_answer[str(number)].values()) < get_question(id_test, number)['Max_count_answer']:
        markup_answer_type_two.add(
            InlineKeyboardButton(text=NEXT_QUESTION, callback_data='next' + '|' + str(number)))
        return markup_answer_type_two
    elif len(dict_answer[str(number)].values()) < get_question(id_test, number)['Min_count_answer']:
        return markup_answer_type_two


def answer_button_type_four(id_test, number):
    '''
        Возвращает объект InlineKeyboardMarkup с вариантами ответов. Для вопросов типа №4.
                Параметры:
                        id_test (str): id теста.
                        number (int): номер вопроса.
                Возвращаемое значение:
                        markup_answer_type_four (set): кнопки с вариантами ответов.
        '''
    markup_type_four = InlineKeyboardMarkup()
    for j in range(get_question(id_test, number)['Diapason_start'], get_question(id_test, number)['Diapason'] + 1):
        markup_type_four.add(InlineKeyboardButton(text=str(j), callback_data=str(
            'c' + str(j))))
    return markup_type_four
