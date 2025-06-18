import grequests
import requests
from bs4 import BeautifulSoup

import json

HEADERS = ['place_overall', 'place_gender', 'place_division', 'name', 'team', 'bib', 'half_time', 'finish_time_net', 'finish_time_gun', 'division', 'state_province']

for year in range(2023, 2025 + 1):
    url = f'https://results.baa.org/{year}/'

    data = {}

    for sex in ['M', 'W', 'X']:
        data[sex] = []
        page = 1
        print(page)
        while True:
            main_r = requests.get(url, params={
                'pid': 'list',
                'pidp': 'start',
                'page': page,
                'event': 'R',
                'event_main_group': 'runner',
                'num_results': 1000,
                'search[sex]': sex,
                'search[age_class]': '%',
            })

            main_soup = BeautifulSoup(main_r.text, 'html.parser')
            for label in main_soup.find_all(class_='list-label'):
                label.decompose()

            ul = main_soup.find('ul', class_='list-group-multicolumn')
            value_list = [[div.text.strip() for div in li.find_all(class_='list-field')[:-1]] for li in ul.find_all('li')[1:]]

            rs = (grequests.get(url + li.find(class_='type-fullname').find('a')['href']) for li in ul.find_all('li')[1:])

            for i, person_r in enumerate(grequests.map(rs)):
                person_soup = BeautifulSoup(person_r.text, 'html.parser')

                division = person_soup.find('td', class_='f-_type_age_class').text.strip()
                state_province = person_soup.find('td', class_='f-state').text.strip()

                value_list[i].extend([division, state_province])
                print(value_list[i])

            data[sex].extend([dict(zip(HEADERS, values)) for values in value_list])

            with open(f'raw/boston-marathon-{year}.json', 'w') as f:
                json.dump(data, f)

            if len(ul.find_all('li')) < 1001:
                break
            page += 1
