import telebot
from model import Model
from textparser import tokenize_data

"""
Telegram bot function producing dialog with the user
"""

# Telegram bot token
with open('TOKENS.txt') as f:
    TOKEN_TG = f.readline()

BOT = telebot.TeleBot(TOKEN_TG)
start_text = "Привет, я бот, который поможет найти нужную информацию на портале вышки. Спроси меня о чем-нибудь и я " \
             "отвечу и найду ссылки :) "

MODEL = Model(True)


# Bot conversation
@BOT.message_handler(commands=['start'])
def send_start(message, text=start_text):
    msg = BOT.send_message(message.from_user.id, text=text)
    BOT.register_next_step_handler(msg, callback_worker_start)


# Returning answer for the question function
def callback_worker_start(call):
    text = ' '.join(tokenize_data(call.text))
    res, link = MODEL.predict(text)
    text_to_user = f'Скорее всего вы сможете найти ответ в этом тексте:\n{res}\n\nИли более подробно ознакомиться с ' \
                   f'этим по ссылке: \n{link} '
    send_start(call, text=text_to_user)


BOT.polling(none_stop=True)
