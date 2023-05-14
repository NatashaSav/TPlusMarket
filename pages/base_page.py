import json
from pathlib import Path

import requests

class BasePage:

    @staticmethod
    def get_all_items_from_response(base_url, INNER_URL, search_phrase, before_all_fixture):
        return before_all_fixture.get(url=f"{base_url}/{INNER_URL}", params={'search': search_phrase}).json()["items"]

    @staticmethod
    def get_json_file():
        file = "large-file.json"
        BASE_DIR = Path(__file__).absolute().parent.parent
        json_file = f'{BASE_DIR}/{file}'
        with open(json_file) as config_file:
            data = json.load(config_file)
        return data

    @staticmethod
    def get_access_token(base_url):
        refresh_url = 'api/auth/refresh'
        my_url = f"{base_url}/{refresh_url}"
        response = requests.get(my_url)
        return response.json()["accessToken"]

    @staticmethod
    def form_header(base_url):
        token = BasePage.get_access_token(base_url)
        header = {'Authorization': 'Bearer {}'.format(token),
                'x-request-app': 'Techno+ Marketplace',
                'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)'
                              ' CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1'}
        return header
