from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from config import LIST_TEST

'''
Объект ReplyKeyboardMarkup с кнопкой запрашивающей контакты пользователя для проверки доступа.
'''
markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
key = KeyboardButton(text=LIST_TEST, request_contact=True)
markup.add(key)
