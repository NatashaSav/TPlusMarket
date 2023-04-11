import pytest
import requests

from pages.base_page import BasePage

INNER_URL = 'api/product/autocomplete'


class TestParametrizedAutocomplete:

    @staticmethod
    @pytest.mark.parametrize("search_phrase, expected_response", [('iPhone 7', ("iрhone" or 'IPhone') and "7"),
                                                                  ('iPhone@7', ("iрhone" or 'IPhone') and "7"),
                                                                  ('iPhone&7', ("iрhone" or 'IPhone') and "7"),
                                                                  ('iPhone*7', ("iрhone" or 'IPhone') and "7"),
                                                                  ('Iphone?7', ("iрhone" or 'IPhone') and "7"),
                                                                  ('Iphone!7', ("iрhone" or 'IPhone') and "7"),
                                                                  ('Iphone...7', ("iрhone" or 'IPhone') and "7"),
                                                                  ('Iphone(7', ("iрhone" or 'IPhone') and "7"),
                                                                  ('Iphone)7', ("iрhone" or 'IPhone') and "7"),
                                                                  ('Iphone:7', ("iрhone" or 'IPhone') and "7"),
                                                                  ('Iphone^7', ("iрhone" or 'IPhone') and "7"),
                                                                  ('Iphone{7', ("iрhone" or 'IPhone') and "7"),
                                                                  ('Iphone}7', ("iрhone" or 'IPhone') and "7"),
                                                                  ('Iphone@#*7', ("iрhone" or 'IPhone') and "7"),
                                                                  ('Iphone%7', ("iрhone" or 'IPhone') and "7")])
    def test_special_symbols_between_words_in_phrase(before_all_fixture, search_phrase, expected_response, base_url):
        items_data = BasePage.get_all_items_from_response(base_url, INNER_URL, search_phrase, before_all_fixture)
        for item in items_data:
            item = item["name"]
            assert expected_response in item, f"expected to see {search_phrase} in actual phrase {item}"

    @staticmethod
    @pytest.mark.parametrize("search_phrase, expected_status_code", [('bluetooth', 401),
                                                                     ('Автомобільний освіжувач повітря', 401),
                                                                     ('Baseus Fabric Artifact Car Fragrance', 401)])
    def test_check_status_code_of_unauthorized_user(search_phrase, expected_status_code, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        params = {'search': search_phrase}
        response = requests.get(url=my_url, params=params)
        assert response.status_code == expected_status_code
        assert response.reason == 'Unauthorized', f"expected status code is {expected_status_code}," \
                                                  f"actual status code is {response.status_code}"

    @staticmethod
    @pytest.mark.parametrize("test_input, expected_response, expected_items_count",
                             [("!@#", 200, 0),
                              ("*&%", 200, 0),
                              ("$%&*", 200, 0),
                              ('fhgjskdnckvj', 200, 0),
                              ('Wk0Dfj14', 200, 0),
                              ('-45678', 200, 0),
                              ('+364', 200, 0),
                              (' ', 200, 0)])
    def test_special_symbols(before_all_fixture, test_input, expected_response, expected_items_count, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        params = {'search': test_input}
        response = before_all_fixture.get(url=my_url, params=params)
        items_data = response.json()["items"]
        assert (len(items_data) == expected_items_count) and response.status_code == expected_response,\
               f"expected items count is {expected_items_count}, " \
               f"actual items count is {items_data}"

    @staticmethod
    @pytest.mark.parametrize("test_input, expected_response, expected_items_count",
                             [("SELECT * FROM users WHERE username = 'john' OR 'a'='a';-- AND password = ''", 200, 0),
                              ("SELECT * FROM db_table WHERE stud_name = %B;", 200, 0),
                              ("SELECT * FROM users WHERE id=1 ; DELETE FROM users;", 200, 0),
                              ("1234 ' AND 1=0 UNION ALL SELECT 'admin', '81dc9bdb52d04dc20036dbd8313ed055", 200, 0)])
    def test_sql_injections(before_all_fixture, test_input, expected_response, expected_items_count, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        params = {'search': test_input}
        response = before_all_fixture.get(url=my_url, params=params)
        items_data = response.json()["items"]
        assert (len(items_data) == expected_items_count) and response.status_code == expected_response, \
               f"expected items count is {expected_items_count}, " \
               f"actual items count is {items_data}"




