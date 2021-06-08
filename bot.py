import telebot
from telebot import types
import os

from game import game_logic as g
from config import TOKEN

bot = telebot.TeleBot(TOKEN, parse_mode=None)

def tg_id(message):
    '''Возвращает id пользователя'''
    return message.chat.id

@bot.message_handler(commands=['start'])
def start(message):
    mci = message.chat.id
    if not os.path.isdir(f'users/{mci}'):
        os.mkdir(f'users/{mci}')

    with open(f'users/{mci}/used_towns.txt', 'w') as f:
        pass

    bot.send_message(mci, 'Давайте поиграем...')

    r = 1#random.randint(0, 1)
    if r == 0:
        bot.send_message(mci, 'Я первый.')
        bot.register_next_step_handler(message, bot_first_move(message))
    else:
        u_f = bot.send_message(mci, 'Вы первый.')
        bot.register_next_step_handler(u_f, human_move)

def bot_first_move(message):
    mci = message.chat.id
    while True:
        town = g.rand_town()
        if g.usage_check(mci, town):
            bot.send_message(mci, town)
            bot.send_message(mci, 'Ваш ход.')
            break

def bot_move(message):
    mci = message.chat.id

def human_move(message):
    mci = message.chat.id
    input_town = message.text
    if g.town_validity(input_town.lower()) and g.usage_check(mci, input_town):
        bot.send_message(mci, 'Окей')
    else:
        incorrect = bot.send_message(mci, 'Не знаю такого города...')
        bot.register_next_step_handler(incorrect, human_move)

bot.polling(none_stop=True)
