import random
import json

from ..dicts import dict_init
from ..config import my_id

dict = dict_init.RU_TOWNS_DICT
all_towns_list = dict_init.RU_TOWNS_LIST


#dict = {'Ф': ['Фатеж', 'Феодосия', 'Фокино', 'Фролово', 'Фрязино', 'Фурманов'], 'О': ["Омск", 'Ольгинск'], 'Х': ['Хорус']}

def rand_town():
    '''Возвращает случайный город'''
    keys = []
    for letter in dict.keys():
        keys.append(letter)

    rand_letter = random.choice(keys)
    rand_town = random.choice(dict[rand_letter])
    return rand_town

def next_town(town):
    '''Возвращает следующий город'''
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

def town_validity(input_town):
    '''Проверяет существование города в базе'''
    if input_town.lower() in all_towns_list:
        return True
    else:
        return False

def letter_validity(town, input_town):
    '''Проверяет введен ли город с нужной буквы'''
    need_letter = town[-1].lower()
    if input_town[0].lower() == need_letter:
        return True
    else:
        return False

def usage_check(town, tg_id):
    '''Проверяет был ли уже назван город. Если нет - записывает в used_towns.txt (lowercase).'''
    while True:
        # Открывает список названных городов
        with open(f'users/{tg_id}/used_towns.txt', 'r', encoding='utf-8') as f1:
            span1 = f1.read()
            span2 = span1.split('_')

            if town.lower() not in span2:
                # Записывает город
                with open(f'users/{tg_id}/used_towns.txt', 'a', encoding='utf-8') as f2:
                    f2.write(town.lower() + '_')
                return True
            else:
                return 'used_town' # Если город уже был назван

def rest_check(letter, tg_id):
    '''Проверяет остались ли еще слова на данную букву'''
    with open(f'users/{tg_id}/used_towns.txt', 'r', encoding='utf-8') as f4:
        span1 = f4.read()
        used_towns = span1.split('_')
        used_towns.remove('')

    used_dict = {}
    first_letters = []
    for t in used_towns: # Создает список всех первых букв использованных городов
        first_letters.append(t[0])

    for l in set(first_letters): # Добавляет в словарь ключи (первые буквы всех использованных городов)
        used_dict[l] = []

    for t in used_towns: # Формирует словарь использованных городов
        f_l = t[0]
        used_dict[f_l].append(t)

    if letter.upper() in dict.keys(): # Есть ли в базе города на букву
        try:
            if set(used_dict[letter.upper()]) != set(dict[letter.upper()]):
                return True # Если города на букву остались
            else:
                return 'all_town_on_letter_used' # Если городов на букву не осталось
        except:
            return True
    else:
        return 'no_letter_dict' # Если буквы нет в словаре

def need_letter(input_town, tg_id):
    '''
    ВОЗВРАЩАЕТ НУЖНУЮ БУКВУ ИЛИ СТРОКУ ОШИБКИ

    Если на последнюю букву input_town не начинается ни один город (из-за
    его присутствия в used_towns.txt), возвращает следующую букву (с конца)
    в названии города (если та также пройдет вышеуказанную проверку).

    Если ни одна буква в названии города не прошла проверку,
    возвращает строку с ошибкой.
    '''
    with open(f'users/{tg_id}/used_towns.txt', 'r', encoding='utf-8') as f3:
        span1 = f3.read()
        used_towns = span1.split('_')

    mod_town = input_town
    town_letter_list = list(mod_town)
    reversed_tll = town_letter_list[::-1]
    last_letter = mod_town[-1]
    counter = 0

    if last_letter.upper() in dict.keys():
        if used_towns:
            for l in reversed_tll: # проходит циклом по всем буквам города (в обратном порядке)
                if l.upper() in dict.keys(): # проверяет есть ли буква в базовом словаре
                    if rest_check(l, tg_id=tg_id) == True:
                        return l.lower()
                    if rest_check(l, tg_id=tg_id) == 'all_town_on_letter_used':
                        counter += 1
                        if counter != len(reversed_tll):
                            continue
                        else:
                            return 'no_available_town'
                    else:
                        return 'no_available_town' # Если больше нет доступных городов
                else:
                    return 'no_letter_dict' # Если буквы нет в базовом словаре
        else:
            return last_letter.lower() # Если буква есть в словаре и еще нет названных городов
    else:
        return 'no_letter_dict' # Если буквы нет в базовом словаре

print(need_letter('Хоф', my_id))

def validity(town, input_town, tg_id):
    '''Возвращает название ошибки или True, если ее нет'''
    if not town_validity(input_town):
        return 'wrong_town'
    elif not letter_validity(town, input_town):
        return 'wrong_letter'
    elif not usage_check(tg_id, town):
        return 'wrong_use'
    else:
        return True

# print(validity('Москва', 'Азов', my_id))

