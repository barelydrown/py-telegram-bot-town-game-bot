import random
import time

import requests
from bs4 import BeautifulSoup
import json

with open('/Users/barely/coding/PyCharmProjects/town_game_bot/tgb/dicts/ru_cities_list.json', 'r') as f:
    ru_towns_list = json.load(f)

towns_count = len(ru_towns_list)

#search_url= 'https://www.google.com/search?q={}+город&oq={}+город&aqs=chrome..69i57j46i13j0i13i30j0i8i13i30l6.7239j0j7&sourceid=chrome&ie=UTF-8'
search_url = 'https://www.google.com/search?q={}+город&oq={}+город'
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
}

def get_html(url, params=None):
    r = requests.get(url, headers=headers, params=params)
    return r.content

def get_town_url(html):
    soup = BeautifulSoup(html, 'html.parser')
    wiki_url = soup.find('div', class_='yuRUbf').find('a')['href']
    return wiki_url


# search_town_request = search_url.format('опочка', 'опочка')
# html = get_html(search_town_request)
# print(html)
# print(search_town_request)
# # print(wiki_url)

def parse():
    url_dict = {}
    counter = 0
    file31 = open('ru_towns_urls_dict.txt', 'a')

    for town in ru_towns_list[746:1117]: #(372)
        true_town = town

        if ' ' in town:
            town = town.replace(' ', '+')

        try:
            search_town_request = search_url.format(town, town)
            html = get_html(search_town_request)
            wiki_url = get_town_url(html)
            url_dict[true_town] = wiki_url
            file31.write(f'\'{true_town}\': \'{wiki_url}\', \n')

            print(f'{true_town} parsed ({counter}/{towns_count})...')
            counter += 1

        except Exception as err:
            file31.write(f'\'{true_town}\': \'no_link\', \n')
            #url_dict[true_town] = 'no_link'
            print(f'ERROR WITH: {true_town} ({town}) \n{err}')

        sleep_time = random.randint(1, 6)
        print(f'sleeping for {sleep_time} sec...')
        time.sleep(sleep_time)
        print('ready!')
        print('='*20)

    file31.close()

    print('DONE')

parse()