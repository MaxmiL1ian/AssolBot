import requests
import json
from config import URL_TEST,URL_CHECK,URL_TESTS,URL_COUNT,URL_ANSWER,URL_QUESTION,URL_RESULT


def get(url, headers, data):
    response = requests.get(url=url, headers=headers, data=data)
    if 200 >= response < 400:
        return json.loads(response.text)



def post(url, headers, data):
    response = requests.get(url=url, headers=headers, data=data)
    if 200 >= response < 400:
        return json.loads(response.text)


def get_check_admission(phone_number):
    '''
        Возвращает id пользователя, если есть доступ.
                Параметры:
                        phone_number (str): номер телефона.
                Возвращаемое значение:
                        (JSON): список тестов or (int) 0.
        '''
    url = URL_CHECK

    contact = phone_number if '+' in phone_number else "+" + phone_number
    payload = json.dumps({
        "phone": contact
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = get(url=url, headers=headers, data=payload)

    return response


def get_tests(user_id):
    '''
        Возвращает список доступных тестов.
                Параметры:
                        user_id (int): id пользователя.
                Возвращаемое значение:
                        (JSON): список тестов.
        '''
    url = URL_TESTS

    payload = json.dumps({
        "id": user_id
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = get(url=url, headers=headers, data=payload)

    return response


def get_test(test_id):
    '''
        Возвращает информацию о тесте.
                Параметры:
                        test_id (int): id теста.
                Возвращаемое значение:
                        (JSON): информация о тесте.
        '''
    url = URL_TEST

    payload = json.dumps({
        "id": test_id
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = get(url=url, headers=headers, data=payload)

    return response


def get_count(test_id):
    '''
        Возвращает кол-во вопросов.
                Параметры:
                        test_id (int): id теста.
                Возвращаемое значение:
                        (JSON): кол-во вопросов.
        '''
    url = URL_COUNT

    payload = json.dumps({
        "id": test_id
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = get(url=url, headers=headers, data=payload)

    return response


def get_question(test_id, question_number):
    '''
        Возвращает информацию о вопросе.
                Параметры:
                        test_id (int): id теста.
                        question_number (int): номер вопроса.
                Возвращаемое значение:
                        (JSON): информация о вопросе.
        '''
    url = URL_QUESTION

    payload = json.dumps({
        "id": test_id,
        "question_num": question_number
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = get(url=url, headers=headers, data=payload)

    return response


def get_answer(question_id):
    '''
        Возвращает варианты ответов.
                Параметры:
                        question_id (int): id вопроса.
                Возвращаемое значение:
                        (JSON): варианты ответов.
        '''
    url = URL_ANSWER

    payload = json.dumps({
        "id": question_id
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = get(url=url, headers=headers, data=payload)

    return response


def send_result(tester_id, test_id, result):
    '''
        Отправляет ответы пользователя в БД.
                Параметры:
                        tester_id (int): id пользователя.
                        test_id (int): id теста.
                        result (dict): ответы.
                Возвращаемое значение:
                        (JSON): код ответа.
        '''
    url = URL_RESULT

    payload = json.dumps({
        "tester_id": tester_id,
        "test_id": test_id,
        "result": str(result)
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = post(url=url, headers=headers, data=payload)

    return response
