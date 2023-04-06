

class BasePage:

    @staticmethod
    def get_all_items_from_response(base_url, INNER_URL, search_phrase, before_all_fixture):
        my_url = f"{base_url}/{INNER_URL}"
        params = {'search': search_phrase}
        response = before_all_fixture.get(url=my_url, params=params)
        items_data = response.json()["items"]
        return items_data