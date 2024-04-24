from tgbot.service import get_test, get_answer, get_question, get_count, get_check_admission, send_result
from tgbot.database import check_user, add_user, del_user, add_test_id, get_id_test, check_answer, add_answer, \
    dict_answer, add_answer_type_two, get_id_user, del_user_by_peer_id
from tgbot.keyboard import test_button, go_test_button, answer_button_type_one, answer_button_type_two_1, \
    answer_button_type_four, answer_button_type_two_2

async def question_type_one(number,user_id):
    return f"<b>Номер вопроса: {number}/{get_count(get_id_test(user_id))}</b>\n<i>{get_question(get_id_test(user_id), number)['Question']}</i>\n<b>Выберите один вариант ответа</b>", answer_button_type_one(
        get_id_test(user_id), number)

async def question_type_two(number,user_id):
    if str(number) in dict_answer(user_id):  # если ответы уже есть, проверяем, что они не превышают макс. допустимое кол-во ответов для данного вопроса, если нет возвращяем текст вопроса и кнопки с ответами
        if len(dict_answer(user_id)[str(number)]) >= get_question(get_id_test(user_id), number)[
            'Max_count_answer']:  # Если кол-во ответов превышает макс. для данного вопроса, то возвращяем False,False и переходим к следующему вопросу. Если нет то возвращяем текст сообщения и кнопки.
            return False, False
        else:
            return f"<b>Номер вопроса: {number}/{get_count(get_id_test(user_id))}</b>\n<i>{get_question(get_id_test(user_id), number)['Question']}</i>\n<b>Выберите от {get_question(get_id_test(user_id), number)['Min_count_answer']} до {get_question(get_id_test(user_id), number)['Max_count_answer']} вариантов ответов</b>", answer_button_type_two_2(
                get_id_test(user_id), number, dict_answer(user_id))
    else:
        return f"<b>Номер вопроса: {number}/{get_count(get_id_test(user_id))}</b>\n<i>{get_question(get_id_test(user_id), number)['Question']}</i>\n<b>Выберите от {get_question(get_id_test(user_id), number)['Min_count_answer']} до {get_question(get_id_test(user_id), number)['Max_count_answer']} вариантов ответов</b>", answer_button_type_two_1(
            get_id_test(user_id), number)

async def question_type_three(number,user_id):
    return f"<b>Номер вопроса: {number}/{get_count(get_id_test(user_id))}</b>\n<i>{get_question(get_id_test(user_id), number)['Question']}</i>\n<b>Ответьте на вопрос сообщением</b>", False

async def question_type_four(number,user_id):
    return f"<b>Номер вопроса: {number}/{get_count(get_id_test(user_id))}</b>\n<i>{get_question(get_id_test(user_id), number)['Question']}</i>\n<b>Выберите число из диапазона от {get_question(get_id_test(user_id), number)['Diapason_start']} до {get_question(get_id_test(user_id), number)['Diapason']}</b>", answer_button_type_four(
        get_id_test(user_id), number)