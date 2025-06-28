import requests
from bs4 import BeautifulSoup

import csv

events = [
    { 'year': 2024, 'filter': 5674 },
    { 'year': 2023, 'filter': 5346 },
    { 'year': 2022, 'filter': 4431 },
]

for event in events:
    url = f'https://www.raceentry.com/results/utah-valley-marathon-and-half-marathon-10k/get-results-report/{event["year"]}'

    page = 0

    headers = None
    results = []

    while True:
        r = requests.post(url, data={
            'filter': event['filter'],
            'search': '',
            'num_results': 100,
            'sort_name': '',
            'sort_order': 'ASC',
            'page': page,
            'additional_filters[edit]': 0
        }, headers={
            'X-Requested-With': 'XMLHttpRequest',
            'Host': 'www.raceentry.com',
        })

        data = r.json()

        soup = BeautifulSoup(data['data'], 'html.parser')

        if headers is None:
            headers = [th.text.strip() for th in soup.find_all('th')]

        for tr in soup.find_all('tr'):
            results.append([td.text.strip() for td in tr.find_all('td')])

        if data['pages'] <= page + 1:
            break
        page += 1

    with open(f'raw/marathons/utah-valley-{event["year"]}.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(results)
