import requests
from bs4 import BeautifulSoup
import json


def chelsea_calendar():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }

    url = 'https://soccer365.ru/clubs/184/'
    response = requests.get(url=url, headers=headers)
    bs = BeautifulSoup(response.text, 'lxml')
    info = bs.find_all('div', class_='game_block')

    calendar_chelsea = {}

    for events in info:
        uid = events.find(class_='game_link').get('dt-id')
        date = events.find('span').text.strip()
        tournament = events.find(class_='cmp').text.strip()
        home = events.find(class_='ht').find('span').text.strip()
        away = events.find(class_='at').find('span').text.strip()
        score_home = events.find(class_='ht').find(class_='gls').text.strip()
        score_away = events.find(class_='at').find(class_='gls').text.strip()

        if home == 'Челси':
            match = 'Челси' + ' - ' + away + ' ' + str(f'({score_home}:{score_away})')
        else:
            match = home + ' - ' + 'Челси' + ' ' + str(f'({score_home}:{score_away})')

        calendar_chelsea[uid] = {
            'date': date,
            'tournament': tournament,
            'match': match
        }

    with open('Marina/football_teams/calendar_chelsea.json', 'w', encoding='utf-8') as file:
        json.dump(calendar_chelsea, file, indent=4, ensure_ascii=False)


def check_updates_chelsea():
    with open("Marina/football_teams/calendar_chelsea.json", encoding='utf-8') as file:
        news_dict = json.load(file)

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }

    url = 'https://soccer365.ru/clubs/184/'
    response = requests.get(url=url, headers=headers)
    bs = BeautifulSoup(response.text, 'lxml')
    info = bs.find_all('div', class_='game_block')

    calendar_chelsea = {}
    fresh_news = {}

    for events in info:
        uid = events.find(class_='game_link').get('dt-id')

        if events in news_dict:
            continue
        else:
            date = events.find('span').text.strip()
            tournament = events.find(class_='cmp').text.strip()
            home = events.find(class_='ht').find('span').text.strip()
            away = events.find(class_='at').find('span').text.strip()
            score_home = events.find(class_='ht').find(class_='gls').text.strip()
            score_away = events.find(class_='at').find(class_='gls').text.strip()

            if home == 'Челси':
                match = 'Челси' + ' - ' + away + ' ' + str(f'({score_home}:{score_away})')
            else:
                match = home + ' - ' + 'Челси' + ' ' + str(f'({score_home}:{score_away})')

            calendar_chelsea[uid] = {
                'date': date,
                'tournament': tournament,
                'match': match
            }

            fresh_news[uid] = {
                'date': date,
                'tournament': tournament,
                'match': match
            }

    with open("Marina/football_teams/calendar_chelsea.json", "w", encoding='utf-8') as file:
        json.dump(calendar_chelsea, file, indent=4, ensure_ascii=False)

    return fresh_news


def main():
    chelsea_calendar()
    check_updates_chelsea()


if __name__ == '__main__':
    main()
