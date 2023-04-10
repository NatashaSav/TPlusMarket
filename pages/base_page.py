import json
from pathlib import Path


class BasePage:

    @staticmethod
    def get_all_items_from_response(base_url, INNER_URL, search_phrase, before_all_fixture):
        my_url = f"{base_url}/{INNER_URL}"
        params = {'search': search_phrase}
        response = before_all_fixture.get(url=my_url, params=params)
        items_data = response.json()["items"]
        return items_data

    @staticmethod
    def get_json_file():
        file = "large-file.json"
        BASE_DIR = Path(__file__).absolute().parent.parent
        json_file = f'{BASE_DIR}/{file}'
        with open(json_file) as config_file:
            data = json.load(config_file)
        return data
