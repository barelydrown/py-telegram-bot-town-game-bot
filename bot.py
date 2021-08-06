import os
import random

import telebot
from telebot import types

import game_logic as g
from config import TOKEN

errors = g.errors
bot = telebot.TeleBot(TOKEN, parse_mode=None)


@bot.message_handler(commands=['start'])
def start(message):
    """Создает папку для пользователя. Выводит на экран кнопки режимов игры"""
    tg_id = message.chat.id
    if not os.path.isdir(f'users/{tg_id}'):
        os.mkdir(f'users/{tg_id}')

    markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                             one_time_keyboard=False,
                                             input_field_placeholder=g.rif)
    towns_ru = types.KeyboardButton('Города 🇷🇺')
    towns_world = types.KeyboardButton('Города 🌎')
    markup_reply.add(towns_ru, towns_world)
    bot.send_message(tg_id, g.start_message,
                     parse_mode='Markdown', reply_markup=markup_reply)


@bot.message_handler(commands=['rules', 'r'])
def show_rules(message):
    bot.send_message(message.chat.id, g.rules, parse_mode='Markdown')


@bot.message_handler(commands=['progress'])
def show_game_progress(message):
    """Отправляет сообщение с ходом игры"""
    used_towns = g.game_progress(message.chat.id)
    game_progress_message = ''
    for town in used_towns:
        game_progress_message += f'{town.title()}\n'
    bot.send_message(message.chat.id, f'Ход игры: \n\n{game_progress_message}')


@bot.message_handler(regexp='Города 🇷🇺')
def ru_mode(message):
    tg_id = message.chat.id
    with open(f'users/{tg_id}/used_towns.txt', 'w') as f:
        pass
    with open(f'users/{tg_id}/cfg.txt', 'w') as f1:
        f1.write('ru')
    first_turn(tg_id)


@bot.message_handler(regexp='Города 🌎')
def world_mode(message):
    tg_id = message.chat.id
    with open(f'users/{tg_id}/used_towns.txt', 'w') as f:
        pass
    with open(f'users/{tg_id}/cfg.txt', 'w') as f1:
        f1.write('world')
    first_turn(tg_id)


@bot.message_handler(content_types=['text'])
def human_turn(message):
    if g.check_mode(message.chat.id):
        input = message.text
        tg_id = message.chat.id
        human_validity(tg_id, input)


def first_turn(tg_id):
    bot.send_message(tg_id, 'Сыграем?')
    r = random.randint(0, 1)
    if r == 0:
        bot.send_message(tg_id, 'Я первый')
        bot_first_turn(tg_id)
    else:
        bot.send_message(tg_id, 'Вы первый')


def need_letter_help(tg_id, town, bot=False):
    '''Возвращает строку ошибки в отредактированном формате'''
    event_code = g.need_letter(town, tg_id)[-1]
    sample_message = errors['need_letter'][event_code]
    pronoun = 'Вам'
    letter_end = 'у'

    if bot == True:
        pronoun = 'мне'

    if event_code == '0':
        need_letter = g.need_letter(town, tg_id)[0].upper()
        help_message = sample_message.format(need_letter)
        return help_message

    if event_code == '1' or event_code == '2':
        need_letter = g.need_letter(town, tg_id)[0].upper()
        wrong_letters = g.need_letter(town, tg_id)[1]
        if len(wrong_letters) > 1:
            letter_end = 'ы'
        help_message = sample_message.format(pronoun, need_letter,
                                             letter_end, wrong_letters)
        return help_message

    if event_code == '3':
        need_letter = g.need_letter(town, tg_id)[0].upper()
        no_dict_letters = g.need_letter(town, tg_id)[1]
        no_town_letters = g.need_letter(town, tg_id)[2]
        help_message = sample_message.format(pronoun, need_letter,
                                             no_dict_letters, no_town_letters)
        return help_message

    if event_code == '4' or event_code == '5':
        no_dict_letters = g.need_letter(town, tg_id)[0]
        no_town_letters = g.need_letter(town, tg_id)[1]
        help_message = sample_message.format(no_dict_letters, no_town_letters)
        return help_message


def human_validity(tg_id, input):
    validity = g.validity(tg_id, input)

    while True:
        if validity == True:
            g.add_town(input, tg_id)
            bot_turn(tg_id, input)
            break

        if validity == 'not_town':
            bot.send_message(tg_id, random.choice(errors['not_town']))
            break

        if validity in errors.keys():
            bot.send_message(tg_id, errors[validity], parse_mode='Markdown')
            break

        if validity == '0':
            last_town = g.usage_check(tg_id, town=input, last=True)
            help_message = need_letter_help(tg_id, last_town)
            print(help_message)
            bot.send_message(tg_id, help_message, parse_mode='Markdown')
            break

        if validity == '1' or validity == '2':
            last_town = g.usage_check(tg_id, town=input, last=True)
            help_message = need_letter_help(tg_id, last_town)
            bot.send_message(tg_id, help_message, parse_mode='Markdown')
            break

        if validity == '3':
            last_town = g.usage_check(tg_id, town=input, last=True)
            help_message = need_letter_help(tg_id, last_town)
            bot.send_message(tg_id, help_message, parse_mode='Markdown')
            break

        if validity == '4' or validity == '5':
            last_town = g.usage_check(tg_id, town=input, last=True)
            help_message = need_letter_help(tg_id, last_town)
            bot.send_message(tg_id, help_message, parse_mode='Markdown')
            break


def bot_first_turn(tg_id):
    bot_town = g.rand_town(tg_id)
    g.add_town(bot_town, tg_id)
    town_link = g.get_link(tg_id, bot_town)
    bot.send_message(tg_id, f'<a href="{town_link}">{bot_town}</a>',
                     parse_mode='HTML', disable_web_page_preview=True)

    next_letter = g.need_letter(bot_town, tg_id)[0]
    if next_letter != bot_town[-1]:
        help_message = need_letter_help(tg_id, bot_town)
        bot.send_message(tg_id, help_message, parse_mode='Markdown')


def bot_try(tg_id, letter):
    while True:
        bot_town = g.town_on_letter(tg_id, letter)

        if g.usage_check(tg_id, town=bot_town) == True:
            return bot_town


def bot_turn(tg_id, human_town):
    event_code = g.need_letter(human_town, tg_id)[-1]

    while True:
        if event_code == '0':
            need_letter = g.need_letter(human_town, tg_id)[0]
            bot_town = bot_try(tg_id, need_letter)
            g.add_town(bot_town, tg_id)
            town_link = g.get_link(tg_id, bot_town)
            bot.send_message(tg_id, f'<a href="{town_link}">{bot_town}</a>',
                             parse_mode='HTML', disable_web_page_preview=True)

            next_letter = g.need_letter(bot_town, tg_id)[0]
            if next_letter != bot_town[-1]:
                help_message = need_letter_help(tg_id, bot_town)
                bot.send_message(tg_id, help_message, parse_mode='Markdown')
            break

        if event_code == '1' or event_code == '2':
            help_message = need_letter_help(tg_id, human_town, bot=True)
            bot.send_message(tg_id, help_message, parse_mode='Markdown')

            need_letter = g.need_letter(human_town, tg_id)[0]
            bot_town = bot_try(tg_id, need_letter)
            g.add_town(bot_town, tg_id)
            town_link = g.get_link(tg_id, bot_town)
            bot.send_message(tg_id, f'<a href="{town_link}">{bot_town}</a>',
                             parse_mode='HTML', disable_web_page_preview=True)
            break

        if event_code == '3':
            help_message = need_letter_help(tg_id, human_town, bot=True)
            bot.send_message(tg_id, help_message, parse_mode='Markdown')

            need_letter = g.need_letter(human_town, tg_id)[0]
            bot_town = bot_try(tg_id, need_letter)
            g.add_town(bot_town, tg_id)
            town_link = g.get_link(tg_id, bot_town)
            bot.send_message(tg_id, f'<a href="{town_link}">{bot_town}</a>',
                             parse_mode='HTML', disable_web_page_preview=True)
            break

        if event_code == '4' or event_code == '5':
            help_message = need_letter_help(tg_id, human_town, bot=True)
            bot.send_message(tg_id, help_message, parse_mode='Markdown')
            break

bot.polling(none_stop=True)