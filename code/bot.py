from datetime import datetime, timedelta
import sqlite3
import telebot
from telebot import types
import pandas as pd
import requests

from tokenize_data import tokenize_data
from model import Model

with open('TOKENS.txt') as f:
    TOKEN_TG = f.readline()

bot = telebot.TeleBot(TOKEN_TG)
start_text = "Привет, я бот, который поможет найти нужную информацию на портале вышки. Спроси меня о чем-нибудь и я " \
             "отвечу и найду ссылки :) "

model = Model(True)


@bot.message_handler(commands=['start'])
def send_start_keyboard(message, text=start_text):
    msg = bot.send_message(message.from_user.id, text=text)
    bot.register_next_step_handler(msg, callback_worker_start)


def callback_worker_start(call):
    text = ' '.join(tokenize_data(call.text))
    res, link = model.predict(text)
    text_to_user = f'Скорее всего вы сможете найти ответ в этом тексте:\n{res}\n\nИли более подробно ознакомиться с ' \
                   f'этим по ссылке: \n{link} '
    send_start_keyboard(call, text=text_to_user)


bot.polling(none_stop=True)
