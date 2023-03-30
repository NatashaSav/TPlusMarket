import requests

INNER_URL = 'api/product/autocomplete'


class TestingAutocomplete:

    @staticmethod
    def test_check_status_of_main_page(before_all_fixture, base_url):
        response = requests.get(url=base_url, verify=False)
        expected_status_code = 200
        assert response.status_code == expected_status_code, f"expected status code is {expected_status_code}, " \
                                                             f"actual status code is {response.status_code}"

    @staticmethod
    def test_check_status_code_of_unauthorized_user(base_url):
        my_url = f"{base_url}/{INNER_URL}"
        params = {'search': 'bluetooth'}
        response = requests.get(url=my_url, params=params)
        expected_status_code = 401
        assert response.status_code == expected_status_code
        assert response.reason == 'Unauthorized', f"expected status code is {expected_status_code}, " \
                                                  f"actual status code is {response.status_code}"

    @staticmethod
    def test_sending_empty_string_to_autocomplete(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        params = {'search': ' '}
        response = before_all_fixture.get(url=my_url, params=params)
        items_data = len(response.json()["items"])
        expected_items_count = 0
        assert items_data == expected_items_count, f"expected items count is {expected_items_count}, " \
                                                   f"actual items count is {items_data}"

    @staticmethod
    def test_sending_incorrect_string_to_autocomplete(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        params = {'search': 'fhgjskdnckvj'}
        response = before_all_fixture.get(url=my_url, params=params)
        items_data = len(response.json()["items"])
        expected_items_count = 0
        assert items_data == expected_items_count, f"expected items count is {expected_items_count}, " \
                                                   f"actual items count is {items_data}"

    @staticmethod
    def test_sending_correct_string_to_autocomplete(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        search_phrase = 'iPhone 7'
        params = {'search': search_phrase}
        response = before_all_fixture.get(url=my_url, params=params)
        items_data = response.json()["items"]
        for item in items_data:
            item = item["name"]
            assert ("iрhone" or 'IPhone') and "7" in item,\
                f"expected to see {search_phrase} in actual phrase {item}"

    @staticmethod
    def test_sending_special_at_sign_symbol_to_autocomplete(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        correct_search_model = 'iPhone 7'
        search_phrase = 'iPhone@7'
        params = {'search': search_phrase}
        response = before_all_fixture.get(url=my_url, params=params)
        items_data = response.json()["items"]
        for item in items_data:
            item = item["name"]
            assert ("iрhone" or 'IPhone') and "7" in item, \
                f"expected to see {correct_search_model} in actual phrase {item}"

    @staticmethod
    def test_sending_special_ampersand_symbol_to_autocomplete(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        correct_search_model = 'iPhone 7'
        search_phrase = 'iPhone&7'
        params = {'search': search_phrase}
        response = before_all_fixture.get(url=my_url, params=params)
        items_data = response.json()["items"]
        for item in items_data:
            item = item["name"]
            assert ("iрhone" or 'IPhone') and "7" in item, \
                f"expected to see {correct_search_model} in actual phrase {item}"

    @staticmethod
    def test_sending_special_asterisk_symbol_to_autocomplete(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        correct_search_model = 'iPhone 7'
        search_phrase = 'iPhone*7'
        params = {'search': search_phrase}
        response = before_all_fixture.get(url=my_url, params=params)
        items_data = response.json()["items"]
        for item in items_data:
            item = item["name"]
            assert ("iрhone" or 'IPhone') and "7" in item, \
                f"expected to see {correct_search_model} in actual phrase {item}"

    @staticmethod
    def test_sending_special_question_mark_symbol_to_autocomplete(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        correct_search_model = 'iPhone 7'
        params = {'search': 'Iphone?7'}
        response = before_all_fixture.get(url=my_url, params=params)
        items_data = response.json()["items"]
        for item in items_data:
            item = item["name"]
            assert ("iрhone" or 'IPhone') and "7" in item,\
                f"expected to see {correct_search_model} in actual phrase {item}"

    @staticmethod
    def test_sending_exclamation_mark_to_autocomplete(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        correct_search_model = 'iPhone 7'
        params = {'search': 'Iphone!7'}
        response = before_all_fixture.get(url=my_url, params=params)
        items_data = response.json()["items"]
        for item in items_data:
            item = item["name"]
            assert ("iрhone" or 'IPhone') and "7" in item, \
                f"expected to see {correct_search_model} in actual phrase {item}"

    @staticmethod
    def test_sending_special_three_dots_symbol_to_autocomplete(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        correct_search_model = 'iPhone 7'
        params = {'search': 'Iphone...7'}
        response = before_all_fixture.get(url=my_url, params=params)
        items_data = response.json()["items"]
        for item in items_data:
            item = item["name"]
            assert ("iрhone" or 'IPhone') and "7" in item, \
                f"expected to see {correct_search_model} in actual phrase {item}"

    @staticmethod
    def test_sending_special_opening_round_quotation_mark_symbol_to_autocomplete(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        correct_search_model = 'iPhone 7'
        params = {'search': 'Iphone(7'}
        response = before_all_fixture.get(url=my_url, params=params)
        items_data = response.json()["items"]
        for item in items_data:
            item = item["name"]
            assert ("iрhone" or 'IPhone') and "7" in item, \
                f"expected to see {correct_search_model} in actual phrase {item}"

    @staticmethod
    def test_sending_special_closing_round_quotation_mark_symbol_to_autocomplete(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        correct_search_model = 'iPhone 7'
        params = {'search': 'Iphone)7'}
        response = before_all_fixture.get(url=my_url, params=params)
        items_data = response.json()["items"]
        for item in items_data:
            item = item["name"]
            assert ("iрhone" or 'IPhone') and "7" in item, \
                f"expected to see {correct_search_model} in actual phrase {item}"

    @staticmethod
    def test_sending_special_colon_sign_symbol_to_autocomplete(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        correct_search_model = 'iPhone 7'
        params = {'search': 'Iphone:7'}
        response = before_all_fixture.get(url=my_url, params=params)
        items_data = response.json()["items"]
        for item in items_data:
            item = item["name"]
            assert ("iрhone" or 'IPhone') in item and "7" in item, \
                f"expected to see {correct_search_model} in actual phrase {item}"

    @staticmethod
    def test_sending_special_caret_symbol_to_autocomplete(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        correct_search_model = 'iPhone 7'
        params = {'search': 'Iphone^7'}
        response = before_all_fixture.get(url=my_url, params=params)
        items_data = response.json()["items"]
        for item in items_data:
            item = item["name"]
            assert ("iрhone" or 'IPhone') and "7" in item, \
                f"expected to see {correct_search_model} in actual phrase {item}"

    @staticmethod
    def test_sending_special_left_curly_bracket_symbol_to_autocomplete(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        correct_search_model = 'iPhone 7'
        params = {'search': 'Iphone{7'}
        response = before_all_fixture.get(url=my_url, params=params)
        items_data = response.json()["items"]
        for item in items_data:
            item = item["name"]
            assert ("iрhone" or 'IPhone') and "7" in item, \
                f"expected to see {correct_search_model} in actual phrase {item}"

    @staticmethod
    def test_sending_special_right_curly_bracket_symbol_to_autocomplete(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        correct_search_model = 'iPhone 7'
        params = {'search': 'Iphone}7'}
        response = before_all_fixture.get(url=my_url, params=params)
        items_data = response.json()["items"]
        for item in items_data:
            item = item["name"]
            assert ("iрhone" or 'IPhone') and "7" in item, \
                f"expected to see {correct_search_model} in actual phrase {item}"

    @staticmethod
    def test_sending_at_sign_number_and_asteriks_symbol_to_autocomplete(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        correct_search_model = 'iPhone 7'
        params = {'search': 'Iphone@#*7'}
        response = before_all_fixture.get(url=my_url, params=params)
        items_data = response.json()["items"]
        for item in items_data:
            item = item["name"]
            assert ("iрhone" or 'IPhone') and "7" in item, \
                f"expected to see {correct_search_model} in actual phrase {item}"

    @staticmethod
    def test_sending_percent_symbol_to_autocomplete(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        correct_search_model = 'iPhone 7'
        params = {'search': 'Iphone%7'}
        response = before_all_fixture.get(url=my_url, params=params)
        items_data = response.json()["items"]
        for item in items_data:
            item = item["name"]
            assert ("iрhone" or 'IPhone') and "7" in item, \
                f"expected to see {correct_search_model} in actual phrase {item}"






