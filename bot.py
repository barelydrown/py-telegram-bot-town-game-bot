import random

import telebot
import os
from random import choice

import game_logic as g
from config import TOKEN, my_id

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
        '1': f'Каежтся {0} на {0}, так как на букву(ы) {0} не начинается ни один город.',
        '2': f'Кажется {0} на {0}, так как на букву(ы) {0} не осталось городов.',
        '3': f'Кажется {0} на {0}, так как на букву(ы) {0} '
           f'не начинается ни один город, а на {0} не осталось городов.',
        '4': f'Кажется игра окончена, так как на букву(ы) {0} не начинается ни один город, '
           f'а на {0} не осталось городов.',
        '5': f'Кажется игра окончена, так как на букву(ы) {0} не начинается ни один город, '
           f'а на {0} не осталось городов.',
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

    r = random.randint(0, 1) # 1
    if r == 0:
        bot.send_message(mci, 'Я первый.')
        bot_first_turn(mci)
    else:
        bot.send_message(mci, 'Вы первый.')

@bot.message_handler(content_types=['text'])
def human_turn(message):
    input = message.text
    tg_id = message.chat.id
    human_validity(tg_id, input)

def human_validity(tg_id, input):
    validity = g.validity(tg_id, input)

    while True:
        if validity == True:
            g.add_town(input, tg_id)
            print('QQ')
            bot_turn(tg_id, input)
            break

        if validity == 'not_town':
            bot.send_message(tg_id, random.choice(errors['not_town']))
            break

        if validity in errors.keys():
            print('ZZZ')
            bot.send_message(tg_id, errors[validity])
            break

        if validity == '1' or validity == '2':
            print('12')
            error = errors['need_letter'][validity]
            need_letter = g.need_letter(input, tg_id)[0]
            incorrect_letters = g.need_letter(input, tg_id)[1]
            error_text = error.format('Вам', need_letter, incorrect_letters)
            bot.send_message(tg_id, error_text)
            break

        if validity == '3':
            print('3')
            error = errors['need_letter'][validity]
            need_letter = g.need_letter(input, tg_id)[0]
            no_dict_letters = g.need_letter(input, tg_id)[1]
            wrong_letters = g.need_letter(input, tg_id)[2]
            error_text = error.format('Вам', need_letter, no_dict_letters, wrong_letters)
            bot.send_message(tg_id, error_text)
            break

        if validity == '4' or validity == '5':
            print('45')
            error = errors['need_letter'][validity]
            no_dict_letters = g.need_letter(input, tg_id)[0]
            wrong_letters = g.need_letter(input, tg_id)[1]
            error_text = error.format(no_dict_letters, wrong_letters)
            bot.send_message(tg_id, error_text)
            break

def bot_first_turn(tg_id):
    bot_town = g.rand_town()
    bot.send_message(tg_id, bot_town)
    g.add_town(bot_town, tg_id)

def bot_turn(tg_id, town):
    while True:
        bot_town = g.next_town(town)
        print(bot_town)
        expected_error = ''
        if bot_validity(tg_id, bot_town) == True:
            if not expected_error:
                bot.send_message(tg_id, bot_town)
                g.add_town(bot_town, tg_id)
                break
            else:
                bot.send_message(tg_id, expected_error)
                bot.send_message(tg_id, bot_town)
                g.add_town(bot_town, tg_id)
                break
        else:
            expected_error = bot_validity(tg_id, bot_town)
            if expected_error[-1] == 'end':
                bot.send_message(tg_id, expected_error[0] + ' Вы победили!')

def bot_validity(tg_id, input):
    validity = g.validity(tg_id, input)

    if validity == True:
        print('QQ')
        return True

    # if validity in errors.keys():
    #     return errors[validity]

    if validity == '1' or validity == '2':
        error = errors['need_letter'][validity]
        need_letter = g.need_letter(input, tg_id)[0]
        incorrect_letters = g.need_letter(input, tg_id)[1]
        error_text = error.format('мне', need_letter, incorrect_letters)
        return error_text

    if validity == '3':
        print('3')
        error = errors['need_letter'][validity]
        need_letter = g.need_letter(input, tg_id)[0]
        no_dict_letters = g.need_letter(input, tg_id)[1]
        wrong_letters = g.need_letter(input, tg_id)[2]
        error_text = error.format('мне', need_letter, no_dict_letters, wrong_letters)
        return error_text

    if validity == '4' or validity == '5':
        print('45')
        error = errors['need_letter'][validity]
        no_dict_letters = g.need_letter(input, tg_id)[0]
        wrong_letters = g.need_letter(input, tg_id)[1]
        error_text = error.format(no_dict_letters, wrong_letters)
        return error_text, 'end'

bot.polling(none_stop=True)