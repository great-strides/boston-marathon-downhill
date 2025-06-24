import requests

import json

events = [
    { 'slug': 'jack-and-jills-downhill', 'id': 'jack-and-jills-downhill-marathon-8' }
]

for event in events:
    for year in range(2022, 2024 + 1):
        page = 1

        base_data = None

        while True:
            print(f'Fetching {event["slug"]} for year {year}, page {page}...')

            r = requests.get(
                f'https://back.runzy.com/mg/event-results/{event["id"]}/?subevent=all&gender=all&age_group=all&page={page}&limit=100&order_by=over_all_place&order_dir=asc&year={year}',
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                }
            )

            if base_data is None:
                base_data = r.json()
            else:
                page_data = r.json()
                base_data['results'].extend(page_data['results'])
            
            if page == base_data['pagination']['last_page']:
                break

            page += 1

        with open(f'raw/marathons/{event["slug"]}-{year}.json', 'w') as f:
            json.dump(base_data, f)
