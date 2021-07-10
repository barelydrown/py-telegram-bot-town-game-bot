import random

import telebot
import os

import game_logic as g
from config import TOKEN

errors = {
    'digit':
        'Мы же в города играем. В вашем ответе не должно быть цифр.',
    'punctuation':
        'Мы же в города играем. В вашем ответе не должно быть спец. символов (кроме "-")',
    'eng':
        'Мы играем в города РФ. В вашем ответе не должно быть латинских символов',
    'not_town': [
        'Такого города нет в моей базе...',
        'Не знаю такого города...',
        'Может вы неправильно написали?'
    ],
    'used_town': 'Кажется этот город уже был...',
    'need_letter': {
        '0': 'Кажется Вам на {}',
        '1': 'Каежтся {} на {},\n так как на букву(ы) {} не начинается ни один город.',
        '2': 'Кажется {} на {},\n так как на букву(ы) {} не осталось городов.',
        '3': 'Кажется {} на {},\n так как на букву(ы) {} '
           'не начинается ни один город, а на {} не осталось городов.',
        '4': 'Кажется игра окончена, так как на букву(ы) {} не начинается ни один город, '
           'а на {} не осталось городов.',
        '5': 'Кажется игра окончена, так как на букву(ы) {} не начинается ни один город, '
           'а на {} не осталось городов.',
    }
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

    r = random.randint(0, 1)
    if r == 0:
        bot.send_message(mci, 'Я первый.')
        bot_first_turn(mci)
    else:
        bot.send_message(mci, 'Вы первый.')

def need_letter_help(tg_id, town, bot=False):
    event_code = g.need_letter(town, tg_id)[-1]
    sample_message = errors['need_letter'][event_code]
    pronoun = 'Вам'

    if bot == True:
        pronoun = 'мне'

    if event_code == '0':
        need_letter = g.need_letter(town, tg_id)[0].upper()
        help_message = sample_message.format(need_letter)
        return help_message

    if event_code == '1' or event_code == '2':
        need_letter = g.need_letter(town, tg_id)[0].upper()
        wrong_letters = g.need_letter(town, tg_id)[1]
        help_message = sample_message.format(pronoun, need_letter, wrong_letters)
        return help_message

    if event_code == '3':
        need_letter = g.need_letter(town, tg_id)[0].upper()
        no_dict_letters = g.need_letter(town, tg_id)[1]
        no_town_letters = g.need_letter(town, tg_id)[2]
        help_message = sample_message.format(pronoun, need_letter, no_dict_letters, no_town_letters)
        return help_message

    if event_code == '4' or event_code == '5':
        no_dict_letters = g.need_letter(town, tg_id)[0]
        no_town_letters = g.need_letter(town, tg_id)[1]
        help_message = sample_message.format(no_dict_letters, no_town_letters)
        return help_message

@bot.message_handler(commands=['progress'])
def show_game_progress(message):
    used_towns = g.game_progress(message.chat.id)
    game_progress_message = ''
    for town in used_towns:
        game_progress_message += f'{town.title()}\n'

    bot.send_message(message.chat.id, f'Ход игры: \n\n{game_progress_message}')

@bot.message_handler(content_types=['text'])
def human_turn(message):
    input = message.text
    tg_id = message.chat.id
    human_validity(tg_id, input)

def human_validity(tg_id, input):
    validity = g.validity(tg_id, input)

    while True:
        if validity == True:
            print('g.validity=True')
            g.add_town(input, tg_id)
            bot_turn(tg_id, input)
            break

        if validity == 'not_town':
            bot.send_message(tg_id, random.choice(errors['not_town']))
            break

        if validity in errors.keys():
            bot.send_message(tg_id, errors[validity])
            break

        if validity == '0':
            last_town = g.usage_check(tg_id, town=input, last=True)
            help_message = need_letter_help(tg_id, last_town)
            bot.send_message(tg_id, help_message)
            break

        if validity == '1' or validity == '2':
            last_town = g.usage_check(tg_id, town=input, last=True)
            help_message = need_letter_help(tg_id, last_town)
            bot.send_message(tg_id, help_message)
            break

        if validity == '3':
            last_town = g.usage_check(tg_id, town=input, last=True)
            help_message = need_letter_help(tg_id, last_town)
            bot.send_message(tg_id, help_message)
            break

        if validity == '4' or validity == '5':
            last_town = g.usage_check(tg_id, town=input, last=True)
            help_message = need_letter_help(tg_id, last_town)
            bot.send_message(tg_id, help_message)
            break

def bot_first_turn(tg_id):
    bot_town = g.rand_town()
    bot.send_message(tg_id, bot_town)
    g.add_town(bot_town, tg_id)

def bot_try(tg_id, letter):
    while True:
        bot_town = g.town_on_letter(letter)

        if g.usage_check(tg_id, town=bot_town) == True:
            return bot_town

def bot_turn(tg_id, human_town):
    event_code = g.need_letter(human_town, tg_id)[-1]

    while True:
        if event_code == '0':
            need_letter = g.need_letter(human_town, tg_id)[0]
            bot_town = bot_try(tg_id, need_letter)
            g.add_town(bot_town, tg_id)
            bot.send_message(tg_id, bot_town)
            break


        if event_code == '1' or event_code == '2':
            help_message = need_letter_help(tg_id, human_town, bot=True)
            bot.send_message(tg_id, help_message)

            need_letter = g.need_letter(human_town, tg_id)[0]
            bot_town = bot_try(tg_id, need_letter)
            g.add_town(bot_town, tg_id)
            bot.send_message(tg_id, bot_town)
            break


        if event_code == '3':
            help_message = need_letter_help(tg_id, human_town, bot=True)
            bot.send_message(tg_id, help_message)

            need_letter = g.need_letter(human_town, tg_id)[0]
            bot_town = bot_try(tg_id, need_letter)
            g.add_town(bot_town, tg_id)
            bot.send_message(tg_id, bot_town)
            break


        if event_code == '4' or event_code == '5':
            help_message = need_letter_help(tg_id, human_town, bot=True)
            bot.send_message(tg_id, help_message)
            break

bot.polling(none_stop=True)