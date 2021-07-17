import json

with open('dicts/ru_cities_dict.json', 'r') as f1:
    RU_TOWNS_DICT = json.load(f1)
    '''
    СЛОВАРЬ ВСЕХ ГОРОДОВ РФ
    Формат: {'первая буква названия города': [список городов начинающихся на букву в ключе]}
    Пример: {'А': ['Азов', 'Аксай'], 'Б': ['Белово', 'Белозерск']}
    '''

with open('dicts/ru_cities_list.json', 'r') as f2:
    RU_TOWNS_LIST = json.load(f2)
    '''
    СПИСОК ВСЕХ ГОРОДОВ РФ
    Формат: [город, город, город]
    Пример: ['азов', 'ак-довурак', 'аксай']
    '''

with open('dicts/punctuation.json', 'r') as f3:
    PUNCTUATION = json.load(f3)
