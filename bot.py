import telebot
import os
from random import choice

import game_logic as g
from config import TOKEN

errors = {
    'digit': '',
    'punctuation': '',
    'eng': '',
    'not_town': [
        'Такого города нет в моей базе...',
        'Не знаю такого города...',
        'Может вы неправильно написали?'
    ],
    'used_town': 'Кажется этот город уже был...',
    'need_letter1': ''
}

bot = telebot.TeleBot(TOKEN, parse_mode=None)

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
        bot.register_next_step_handler(u_f, input_validity)

def input_validity(message):
    if g.is_text(message.text) == True:
        return True
    if g.is_text(message.text) == 'digit':
        bot.send_message(message.chat.id, 'Мы же в города играем. В вашем ответе не должно быть цифр.')
    if g.is_text(message.text) == 'punctuation':
        bot.send_message(message.chat.id, 'Мы же в города играем. В вашем ответе не должно быть '
                                          'спец. символов (кроме "-")')
    if g.is_text(message.text) == 'eng':
        bot.send_message(message.chat.id, 'Мы играем в города РФ. В вашем ответе не должно быть '
                                          'латинских символов')

@bot.message_handler(content_types=['text'], func=input_validity)
def is_town(message):
    town = message.text
    if g.town_validity(town):
        return True
    else:
        bot.send_message(message.chat.id, choice(errors['not_town']))

@bot.message_handler(content_types=['text'], func=is_town)
def human_first_move(message):
    human_town = message.text
    g.add_town(human_town, message.chat.id)
    bot_first_move2(message)

def bot_first_move2(message):
    human_town = message.text
    bot_town = g.next_town(human_town)
    g.add_town(bot_town, message.chat.id)
    human_move(message, human_town, bot_town)


def town_validity(message, input_town, answer_town):
    ''''''
    tg_id = message.chat.id
    need = g.need_letter(input_town, tg_id)

    if g.usage_check(answer_town, tg_id) == True:
        if need[0] == answer_town[0]:
            return True
        elif need[-1] == 1:
            bot.send_message(tg_id, f'Каежтся вам на {need[0].upper()}, так как на букву(ы) {need[1].upper()} '
                                    f'не начинается ни один город.')
        elif need[-1] == 2:
            bot.send_message(tg_id, f'Кажется вам на {need[0].upper()}, так как на букву(ы) {need[1].upper()} '
                                    f'не осталось городов.')
        elif need[-1] == 3:
            bot.send_message(tg_id, f'Кажется вам на {need[0].upper()}, так как на букву(ы) {need[1].upper()} '
                                    f'не начинается ни один город, а на {need[2]} не осталось городов.')
        else:
            bot.send_message(tg_id, f'Кажется игра окончена, так как на букву(ы) {need[0].upper()} '
                                    f'не начинается ни один город, а на {need[1]} не осталось городов.')
    else:
        bot.send_message(tg_id, errors['used_town'])

# @bot.message_handler(content_types=['text'], func=town_validity)
def human_move(message, human_town, bot_town):



bot.polling(none_stop=True)
