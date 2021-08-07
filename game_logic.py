import random
from string import digits

import dict_init

start_message = dict_init.start_message
help_message = dict_init.help_message
info_message = dict_init.info_message
rif = dict_init.reply_input_field
rules = dict_init.rules
punctuation = dict_init.PUNCTUATION
errors = dict_init.errors


def get_data(tg_id):
    """Определяет режим игры и возвращает необходимые данные"""
    with open(f'users/{tg_id}/mode.txt', 'r') as f1:
        mode = f1.read()
    if mode == 'ru':  # Города РФ
        dict = dict_init.RU_TOWNS_DICT
        all_towns_list = dict_init.RU_TOWNS_LIST
        links = dict_init.LINKS
        return dict, all_towns_list, links, 'ru'

    if mode == 'world':  # Города мира
        dict = dict_init.TOWNS_DICT
        all_towns_list = dict_init.TOWNS_LIST
        links = None
        return dict, all_towns_list, links, 'world'


def is_text(input):
    """
    Аргументом может быть только строка. Проверяет строку на наличие
    цифр и символов. Возвращает True или название ошибки.
    """
    for s in list(input):
        if s in list(digits):
            return 'digit'
        if s in punctuation:
            return 'punctuation'
        else:
            return True


def rand_town(tg_id):
    """Возвращает случайный город"""
    dict = get_data(tg_id)[0]
    keys = []
    for letter in dict.keys():
        keys.append(letter)

    rand_letter = random.choice(keys)
    rand_town = random.choice(dict[rand_letter])
    return rand_town


def next_town(tg_id, town):
    """
    Возвращает случайный город, который начинается на последнюю
    букву города в аргументе.
    """
    dict = get_data(tg_id)[0]
    letters_len = len(town)
    mod_town = town

    for letter in range(letters_len):
        last_letter = mod_town[-1].upper()
        if last_letter in dict.keys():
            all_vars = dict[last_letter]
            n_town = random.choice(all_vars)
            return n_town
        else:
            mod_town = list(mod_town)
            mod_town.remove(mod_town[-1])
            mod_town = ''.join(mod_town)


def town_validity(tg_id, input_town):
    """Проверяет существование города в базе"""
    all_towns_list = get_data(tg_id)[1]
    if input_town.lower() in all_towns_list:
        return True


def letter_validity(town, input_town):
    """Проверяет введен ли город с нужной буквы"""
    need_letter = town[-1].lower()
    if input_town[0].lower() == need_letter:
        return True


def usage_check(tg_id, town=None, last=False):
    """
    Открывает список названных городов. Если список пустой,
    возвращает соответствующую строку сценария.
    Если список не пустой, проверяет был ли уже назван город.
    Если параметр last=True, возвращает последний названный город.
    """
    with open(f'users/{tg_id}/used_towns.txt', 'r', encoding='utf-8') as f1:
        span1 = f1.read()
        span2 = span1.split('_')
        span2.remove('')

        if span1:
            if last == True:
                return span2[-1]

            if town.lower() not in span2:
                return True  # Если город еще не был назван
            else:
                return 'used_town'  # Если город уже был назван
        else:
            return 'first_turn'  # Если список названных городов пустой


def last_town(tg_id):
    """Возвращает последний город"""
    with open(f'users/{tg_id}/used_towns.txt', 'r', encoding='utf-8') as f1:
        span1 = f1.read()
        span2 = span1.split('_')
        span2.remove('')
        return span2[-1]


def add_town(town, tg_id):
    """Записывает город в текстовой файл с названными городами"""
    with open(f'users/{tg_id}/used_towns.txt', 'a', encoding='utf-8') as f2:
        f2.write(town.lower() + '_')


def game_progress(tg_id):
    """Возвращает список всех использованных городов"""
    with open(f'users/{tg_id}/used_towns.txt', 'r', encoding='utf-8') as f1:
        span1 = f1.read()
        span2 = span1.split('_')
        span2.remove('')
        return span2


def letter_existence(tg_id, letter):
    """
    Проверяет существование городов, начинающихся
    на букву, указанную в аргументе.
    """
    dict = get_data(tg_id)[0]
    if letter.upper() in dict.keys():
        return True


def rest_check(letter, tg_id):
    """Проверяет остались ли еще города на данную букву"""
    dict = get_data(tg_id)[0]
    with open(f'users/{tg_id}/used_towns.txt', 'r', encoding='utf-8') as f4:
        span1 = f4.read()
        used_towns = span1.split('_')
        used_towns.remove('')
        used_towns_up = []
        for to in used_towns:
            used_towns_up.append(to.title())

    used_dict = {}
    first_letters = []
    for t in used_towns_up:  # Создает список всех первых букв
        # использованных городов
        first_letters.append(t[0])

    for l in set(first_letters):  # Добавляет в словарь ключи (первые буквы
        # всех использованных городов)
        used_dict[l] = []

    for t in used_towns_up:  # Формирует словарь использованных городов
        f_l = t[0]
        used_dict[f_l].append(t)

    if letter_existence(tg_id, letter):  # Есть ли в базе города на букву
        try:
            if set(used_dict[letter.upper()]) != set(dict[letter.upper()]):
                return True  # Если города на букву остались
            else:
                return 'all_town_on_letter_used'  # Если городов на букву не
                # осталось
        except:
            return True
    else:
        return 'no_letter_dict'  # Если буквы нет в словаре


def need_letter(town, tg_id):
    """
    Возвращает нужную букву (буквы не прошедшие проверку) и номер сценария.

    Если на последнюю букву town не начинается ни один город (из-за
    его присутствия в used_towns.txt), возвращает следующую букву (с конца)
    в названии города (если та также пройдет вышеуказанную проверку).

    Если ни одна буква в названии города не прошла проверку, возвращает
    списки непрошедших проверку букв, а также номер сценария.
    """
    town_letter_list = list(town)
    reversed_tll = town_letter_list[::-1]
    no_dict_letters = []  # Список букв, на которые не начинается ни один город
    wrong_letters = []  # Список букв, на которые не осталось городов

    for l in reversed_tll:
        if rest_check(l, tg_id=tg_id) != 'no_letter_dict':
            if rest_check(l, tg_id=tg_id) != 'all_town_on_letter_used':
                if rest_check(l, tg_id=tg_id) == True:
                    if not no_dict_letters and not wrong_letters:
                        return l.lower(), '0'
                    if no_dict_letters:
                        return l.lower(), wrong_trans(no_dict_letters), '1'
                    if wrong_letters:
                        return l.lower(), wrong_trans(wrong_letters), '2'
                    else:
                        return l.lower(), wrong_trans(no_dict_letters), \
                               wrong_trans(wrong_letters), '3'
            else:
                wrong_letters.append(l)
                if len(no_dict_letters + wrong_letters) == len(town):
                    return no_dict_letters, wrong_letters, '4'
        else:
            no_dict_letters.append(l)
            if len(no_dict_letters + wrong_letters) == len(town):
                return no_dict_letters, wrong_letters, '5'


def validity(tg_id, input):
    """Возвращает строку/номер ошибки или True, если ее нет"""
    if is_text(input) == True:
        if town_validity(tg_id, input):
            use_check = usage_check(tg_id, town=input)
            if use_check == 'first_turn':
                return True

            if use_check == True:
                first_letter = input[0].lower()
                answer = usage_check(tg_id, town=input, last=True)
                need = need_letter(answer, tg_id)
                if need[0] == first_letter:
                    return True
                else:
                    return need[-1]

            if use_check == 'used_town':
                return 'used_town'
        else:
            return 'not_town'
    else:
        return is_text(input)


def wrong_trans(letter_list):
    """Превращает список неверных букв в строку с запятыми"""
    new_string = ''
    if len(letter_list) <= 1:
        new_string = f'{letter_list[0].upper()}'
    else:
        for letter in letter_list:
            new_string += f'{letter.upper()}' + ', '
    return new_string


def town_on_letter(tg_id, letter):
    """Возвращает случайный город на букву в аргументе"""
    dict = get_data(tg_id)[0]
    upper_letter = letter.upper()
    return random.choice(dict[upper_letter])


def google_link(town):
    """Формирует поисковой запрос Google"""
    link = f'https://www.google.com/search?q={town}+город'
    return link


def get_link(tg_id, town):
    """Возвращает ссылку на город в аргументе"""
    if get_data(tg_id)[-1] == 'ru':
        links = get_data(tg_id)[2]
        try:
            return links[town.lower()]
        except:
            return None
    else:
        return google_link(town)


def check_mode(tg_id):
    """Возвращает True, если выбран режим игры"""
    with open(f'users/{tg_id}/mode.txt', 'r') as file:
        mode = file.read()
        if mode:
            return True
