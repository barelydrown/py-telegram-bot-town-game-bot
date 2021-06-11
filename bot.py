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

# def lul(message):
#     return True
#
# @bot.message_handler(func=lul)
# def lul1(message):
#     bot.send_message(message.chat.id, 'woooow')

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
    else:
        u_f = bot.send_message(mci, 'Вы первый.')
        #bot.register_next_step_handler(u_f, input_validity)

@bot.message_handler(content_types=['text'])
def smth(message):
    input = message.text
    tg_id = message.chat.id
    human_validity(tg_id, input)

# @bot.message_handler(content_types=['text'])
# def input_validity(tg_id, input):
#     input_town = input
#
#     if g.is_text(input_town) == True:
#         if g.town_validity(input_town):
#             use_check = g.usage_check(tg_id, town=input_town)
#             if use_check == 'first_move':
#                 g.add_town(input_town, tg_id)
#                 bot_move(input_town, tg_id)
#
#             if use_check == 'used_town':
#                 bot.send_message(tg_id, errors['used_town'])
#
#             if use_check == True:
#                 first_letter = input_town[0].lower()
#                 answer = g.usage_check(tg_id, town=input_town, last=True)
#                 need = g.need_letter(answer, tg_id)
#                 print(first_letter, need)
#                 if need == first_letter:
#                     bot.send_message(tg_id, 'ВСЕ ВЕРНО!')
#                     bot_move(input_town, tg_id)
#                     return True
#                 if need[-1] == 1:
#                     bot.send_message(tg_id, f'Каежтся вам на {need[0].upper()}, так как на букву(ы) {need[1].upper()} '
#                                             f'не начинается ни один город.')
#                 if need[-1] == 2:
#                     bot.send_message(tg_id, f'Кажется вам на {need[0].upper()}, так как на букву(ы) {need[1].upper()} '
#                                             f'не осталось городов.')
#                 if need[-1] == 3:
#                     bot.send_message(tg_id, f'Кажется вам на {need[0].upper()}, так как на букву(ы) {need[1].upper()} '
#                                             f'не начинается ни один город, а на {need[2]} не осталось городов.')
#                 if need[-1] == 4:
#                     bot.send_message(tg_id, f'Кажется игра окончена, так как на букву(ы) {need[0].upper()} '
#                                             f'не начинается ни один город, а на {need[1]} не осталось городов.')
#                 if need[-1] == 5:
#                     bot.send_message(tg_id, f'Кажется игра окончена, так как на букву(ы) {need[0].upper()} '
#                                             f'не начинается ни один город, а на {need[1]} не осталось городов.')
#         else:
#             bot.send_message(tg_id, choice(errors['not_town']))
#     else:
#         print('111')
#         error = errors[g.is_text(input_town)]
#         bot.send_message(tg_id, error)

# def input_validity(input, id):
#     tg_id = id
#
#     if g.is_text(input) == True:
#         if g.town_validity(input):
#             use_check = g.usage_check(input, tg_id)
#             if g.usage_check(input, tg_id, first=True) == 'first_town':
#                 g.add_town(input, tg_id)
#                 bot_first_move(input, tg_id)
#             if use_check == True:
#                 print('QQQ')
#                 first_letter = input[0].lower()
#                 need = g.need_letter(input, tg_id)
#                 if need == first_letter:
#                     bot.send_message(tg_id, 'ВСЕ ВЕРНО!')
#                     return True
#                 if need[-1] == 1:
#                     bot.send_message(tg_id, f'Каежтся вам на {need[0].upper()}, так как на букву(ы) {need[1].upper()} '
#                                             f'не начинается ни один город.')
#                 if need[-1] == 2:
#                     bot.send_message(tg_id, f'Кажется вам на {need[0].upper()}, так как на букву(ы) {need[1].upper()} '
#                                             f'не осталось городов.')
#                 if need[-1] == 3:
#                     bot.send_message(tg_id, f'Кажется вам на {need[0].upper()}, так как на букву(ы) {need[1].upper()} '
#                                             f'не начинается ни один город, а на {need[2]} не осталось городов.')
#                 if need[-1] == 4:
#                     bot.send_message(tg_id, f'Кажется игра окончена, так как на букву(ы) {need[0].upper()} '
#                                             f'не начинается ни один город, а на {need[1]} не осталось городов.')
#                 if need[-1] == 5:
#                     bot.send_message(tg_id, f'Кажется игра окончена, так как на букву(ы) {need[0].upper()} '
#                                             f'не начинается ни один город, а на {need[1]} не осталось городов.')
#             else:
#                 print('ZZZ')
#                 bot.send_message(tg_id, errors['used_town'])
#         else:
#             bot.send_message(tg_id, choice(errors['not_town']))
#
#     if g.is_text(input) == 'digit':
#         bot.send_message(input, 'Мы же в города играем. В вашем ответе не должно быть цифр.')
#
#     if g.is_text(input) == 'punctuation':
#         bot.send_message(input, 'Мы же в города играем. В вашем ответе не должно быть '
#                                           'спец. символов (кроме "-")')
#
#     if g.is_text(input) == 'eng':
#         bot.send_message(tg_id, 'Мы играем в города РФ. В вашем ответе не должно быть '
#                                           'латинских символов')

def human_validity(tg_id, input):
    validity = g.validity(tg_id, input)

    while True:
        if validity == True:
            g.add_town(input, tg_id)
            print('QQ')
            bot_move(tg_id, input)
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
            error_text = error.format('Вам', no_dict_letters, wrong_letters)
            bot.send_message(tg_id, error_text)
            break

def bot_validity(tg_id, input):
    pass

def bot_move(tg_id, town):
    human_town = town
    bot_town = g.next_town(human_town)
    g.add_town(bot_town, tg_id)
    bot.send_message(tg_id, bot_town)

# @bot.message_handler(content_types=['text'], func=input_validity)
# def is_town(message):
#     town = message.text
#     if g.town_validity(town):
#         pass
#     else:
#         bot.send_message(message.chat.id, choice(errors['not_town']))

# @bot.message_handler(func=is_town)
# def human_first_move(message):
#     human_town = message.text
#     g.add_town(human_town, message.chat.id)
#     bot_first_move2(message)
#
# def bot_first_move2(message):
#     human_town = message.text
#     bot_town = g.next_town(human_town)
#     g.add_town(bot_town, message.chat.id)
#     bot.send_message(message.chat.id, bot_town)
#     # town_validity(message, human_town, bot_town)

# def town_validity(message, input_town, answer_town):
#     ''''''
#     tg_id = message.chat.id
#     need = g.need_letter(input_town, tg_id)
#
#     if g.usage_check(answer_town, tg_id) == True:
#         if need[0] == answer_town[0]:
#             return True
#         elif need[-1] == 1:
#             bot.send_message(tg_id, f'Каежтся вам на {need[0].upper()}, так как на букву(ы) {need[1].upper()} '
#                                     f'не начинается ни один город.')
#         elif need[-1] == 2:
#             bot.send_message(tg_id, f'Кажется вам на {need[0].upper()}, так как на букву(ы) {need[1].upper()} '
#                                     f'не осталось городов.')
#         elif need[-1] == 3:
#             bot.send_message(tg_id, f'Кажется вам на {need[0].upper()}, так как на букву(ы) {need[1].upper()} '
#                                     f'не начинается ни один город, а на {need[2]} не осталось городов.')
#         else:
#             bot.send_message(tg_id, f'Кажется игра окончена, так как на букву(ы) {need[0].upper()} '
#                                     f'не начинается ни один город, а на {need[1]} не осталось городов.')
#     else:
#         bot.send_message(tg_id, errors['used_town'])
#
# @bot.message_handler(content_types=['text'], func=town_validity)
# def human_move(message):
#     human_town = message.text
#     g.add_town(human_town, message.chat.id)
#     bot_move(human_town)
#
# def bot_move(message):
#     human_town = message.text
#     bot_town = g.next_town(human_town)
#     g.add_town(bot_town, message.chat.id)
#     bot.send_message(message.chat.id, bot_town)



bot.polling(none_stop=True)
