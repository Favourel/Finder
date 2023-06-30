# utils.py

import requests


def get_visitor_location(ip_address):
    ipinfo_api_key = 'f2d2b2edba9968'  # Get your API key by signing up at https://ipinfo.io/signup

    url = f'https://ipinfo.io/{ip_address}?token={ipinfo_api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(data.get('city'))
        return {
            'city': data.get('city'),
            'region': data.get('region'),
            'country': data.get('country'),
            "timezone": data.get('timezone')
        }
    # return None
