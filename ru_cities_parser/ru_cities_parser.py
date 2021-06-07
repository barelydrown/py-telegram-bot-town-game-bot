import requests
from bs4 import BeautifulSoup
import json

HOST = 'https://gorodarus.ru/'
URL = 'https://geogoroda.ru/rossiya/bukva/'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
    'accept': '*/*'
}

def get_urls():
    '''Возвращает список ссылок на страницы со всеми городами'''
    with open('all_letters_list.json', 'r', encoding='utf-8') as l_json:
        letters = json.load(l_json)

    all_urls = []
    for letter in letters:
        all_urls.append(URL + letter)

    return all_urls

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_html_content(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r.content

def get_all_letters(html):
    '''Создает список первых букв городов и записывает его в json-файл'''
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find('h4', class_='goroda-bukva').get_text(strip=True)

    pages =[]
    for n in pagination:
        pages.append(n.lower())

    with open('all_letters_list.json', 'w', encoding='utf-8') as l_json:
        json.dump(pages, l_json)

def parse():
    '''
    Парсит названия всех городов на всевозможные буквы, записывает
    значения в словарь, где ключом является буква, а значением список
    городов, начинающихся на эту букву. Затем записывает данный словарь в json-файл.
    '''
    URLS = get_urls()
    main_dict = {}
    letter_list = []

    for url in URLS:
        html = get_html_content(url)
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('td', class_='views-field views-field-title large')
        letter = url[-1].upper()

        for item in items:
            letter_list.append(item.find('a').get_text())

            main_dict[letter] = letter_list

        letter_list = []

    with open('ru_cities_dict.json', 'w', encoding='utf-8') as file:
        json.dump(main_dict, file)

    return print(main_dict)

parse()