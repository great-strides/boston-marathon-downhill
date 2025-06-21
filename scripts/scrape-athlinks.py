import requests

import json
import os

events = [
    { 'slug': 'sundance-to-spearfish-2025', 'event': 1088574, 'race': 2506674 },
    { 'slug': 'sundance-to-spearfish-2024', 'event': 1059767 },
    { 'slug': 'sundance-to-spearfish-2023', 'event': 1030813 },
    { 'slug': 'leading-ladies-2025', 'event': 1086802 },
    { 'slug': 'leading-ladies-2024', 'event': 1042087 },
    { 'slug': 'leading-ladies-2023', 'event': 1025465 },
    { 'slug': 'jack-and-jills-downhill-2025', 'event': 1069347 },
    { 'slug': 'tucson-marathon-2025', 'event': 1066702 },
    { 'slug': 'tucson-marathon-2024', 'event': 1037732 },
    { 'slug': 'tucson-marathon-2023', 'event': 994188 },
    { 'slug': 'pocatello-2025', 'event': 1084635, 'race': 2489475 },
    { 'slug': 'pocatello-2024', 'event': 1056754, 'race': 2385153 },
    { 'slug': 'pocatello-2023', 'event': 1026520, 'race': 2277436 },
    { 'slug': 'hawaii-bird-conservation-2025', 'event': 1067174, 'race': 2421878 },
]

for event in events:
    if os.path.exists(f'raw/marathons/{event["slug"]}.json'):
        print(f'Skipping {event["slug"]}...')
        continue

    print(event['slug'])
    from_ = 0

    base_data = None

    while True:
        print(f'Fetching from {from_}...')
        
        r = requests.get(f'https://reignite-api.athlinks.com/event/{event["event"]}{"/race/" + str(event["race"]) if event.get("race") else ""}/results?from={from_}&limit=100')

        if base_data is None:
            base_data = r.json()
            if type(base_data) is list:
                base_data = base_data[0]
        else:
            page_data = r.json()
            if type(page_data) is list:
                page_data = page_data[0]
            for interval in page_data['intervals']:
                for base_interval in base_data['intervals']:
                    if interval['id'] == base_interval['id']:
                        base_interval['results'].extend(interval['results'])
                        break

        if base_data['division']['totalAthletes'] < from_ + 100:
            break
        from_ += 100

    with open(f'raw/marathons/{event["slug"]}.json', 'w') as f:
        json.dump(base_data, f)
