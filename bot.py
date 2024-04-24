import asyncio

from telebot.async_telebot import AsyncTeleBot
from config import START_MESSAGE, TOKEN

from tgbot.keyboard import markup
from tgbot.gluing import access_verification, information_test, send_question, set_answer, set_answer_type_three, \
    set_answer_type_two, add_id_test

'''
Создаётся объект AsyncTeleBot.
'''

bot = AsyncTeleBot(TOKEN, parse_mode='HTML')


@bot.message_handler(commands=['start'])
async def any_user(message):
    await bot.send_message(
        message.from_user.id,
        text=START_MESSAGE,
        reply_markup=markup
    )


@bot.message_handler(content_types=[
    'contact'])  # Функция после получения номера телефона, проверяет доступ и выдаёт список доступных тестов
async def contact(message):
    msg, button = await access_verification(message.contact.phone_number, message.from_user.id)
    await bot.send_message(message.chat.id, text=f'{msg}', reply_markup=button)


async def questions(i, user_id, message):  # Функция выдаёт текст вопроса, и кнопки ответы
    msg, button = await send_question(i, user_id)
    if button == 'end':  # Если возвращяется end вместо кнопки, то завершаем тест
        await bot.send_message(message.chat.id, text=f'{msg}')
    elif msg and button:  # Выдаёт вопрос и кнопки
        await bot.send_message(message.chat.id, text=f'{msg}', reply_markup=button)
    elif msg and not button:  # выдаёт вопрос типа 3
        await bot.send_message(message.chat.id, text=f'{msg}')
        bot.register_message_handler(answer_tree)  # обрпботчик нового сообщения для ответа на вопрос 3-го типа
    else:  # Если вернулся False,False, то переходим к следующему вопросу
        await questions(i + 1, user_id, message)


async def answer_tree(message):  # Обработчик ответа сообщением на вопросы типа 3
    number = await set_answer_type_three(message.from_user.id, message.text)
    await bot.delete_message(message.chat.id, message.message_id - 1)
    await bot.delete_message(message.chat.id, message.message_id)
    await questions(number + 1, message.from_user.id, message)


@bot.callback_query_handler(func=lambda call: True)  # Обработчик нажатия на кнопки
async def query_handler(call):
    if call.message:
        if call.data[0:1] == 't':
            msg, button = await information_test(call.data[1:])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'{msg}',
                                        reply_markup=button)
        elif call.data[0:1] == 'g':  # Обработчик нажатия на кнопку запуска. Запускает выполнение теста
            await add_id_test(call.from_user.id, call.data[1:])
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await questions(1, call.from_user.id, call.message)
        elif call.data[
             0:1] == 'a':  # обработчик нажатия на кнопку с вариантом ответа вопрос типа 1 (Находит вариант ответа, и добавляет его в таблицу БД)
            number = await set_answer(call.from_user.id, call.data[1:])
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await questions(number + 1, call.from_user.id, call.message)
        elif call.data[
             0:1] == 'c':  # обработчик нажатия на кнопку с вариантом ответа вопрос типа 3 (Находит вариант ответа, и добавляет его в таблицу БД)
            number = await set_answer_type_three(call.from_user.id, call.data[1:])
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await questions(number + 1, call.from_user.id, call.message)
        elif call.data[
             0:1] == 'd':  # обработчик нажатия на кнопку с вариантом ответа вопрос типа 2 (Находит вариант ответа, и добавляет его в таблицу БД)
            number = await set_answer_type_two(call.from_user.id, call.data[1:])
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await questions(number, call.from_user.id, call.message)

        elif call.data == 'disenable':  # обработчик нажатия на уже активную кнопку в вопросе типа 2.
            pass

        elif call.data.split('|')[
            0] == 'next':  # обработчик нажатия на кнопку "Следующий вопрос" в вопросах типа 2. Запускает выполнение следующего вопроса.
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await questions(int(call.data.split('|')[1]) + 1, call.from_user.id, call.message)


async def main():
    print('bot start')
    await bot.infinity_polling()



if __name__ == "__main__":
    asyncio.run(main())
