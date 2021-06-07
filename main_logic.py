import random
import json

def rand_town():
    '''Возвращает случайный город'''
    with open('ru_cities_parser/ru_cities_dict.json', 'r') as d_json:
        dict = json.load(d_json)

    keys = []
    for letter in dict.keys():
        keys.append(letter)

    rand_letter = random.choice(keys)
    rand_town = random.choice(dict[rand_letter])

    return rand_town

def usage_check(tg_id, town):
    '''Проверяет был ли уже назван город. Записывает, если нет.'''
    while True:
        # Открывает список названных городов
        with open(f'users/{tg_id}/used_towns.txt', 'r', encoding='utf-8') as f1:
            span1 = f1.read()
            span2 = span1.split('_')

            if town not in span2:
                # Записывает город
                with open(f'users/{tg_id}/used_towns.txt', 'a', encoding='utf-8') as f2:
                    f2.write(town + '_')
                return True
            else:
                return False

def town_validity(input_town):
    '''Проверяет существование города'''
    with open('ru_cities_parser/ru_cities_list.json', 'r') as l_json:
        all_towns = json.load(l_json)

    if input_town in all_towns:
        return True
    else:
        return False