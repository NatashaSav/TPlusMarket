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
    @pytest.mark.autocomplete
    def test_special_symbols_between_words_in_phrase(before_all_fixture, search_phrase, expected_response, base_url):
        items_data = BasePage.get_all_items_from_response(base_url, INNER_URL, search_phrase, before_all_fixture)
        assert all(list(filter(lambda item: expected_response in item["name"], items_data))), \
               f"{expected_response} is not in {search_phrase}"

    @staticmethod
    @pytest.mark.parametrize("search_phrase, expected_status_code", [('bluetooth', 401),
                                                                     ('Автомобільний освіжувач повітря', 401),
                                                                     ('Baseus Fabric Artifact Car Fragrance', 401)])
    @pytest.mark.autocomplete
    def test_check_status_code_of_unauthorized_user(search_phrase, expected_status_code, base_url):
        response = requests.get(url=f"{base_url}/{INNER_URL}", params={'search': search_phrase})
        assert response.status_code == expected_status_code and response.reason == 'Unauthorized', \
            f"expected status code is {expected_status_code}," f"actual status code is {response.status_code}"

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
    @pytest.mark.autocomplete
    def test_special_symbols(before_all_fixture, test_input, expected_response, expected_items_count, base_url):
        response = before_all_fixture.get(url=f"{base_url}/{INNER_URL}", params={'search': test_input})
        items_data = response.json()["items"]
        assert response.status_code == expected_response, f"status code is not {expected_response}"
        assert all(list(filter(lambda item: (len(items_data) == expected_items_count), items_data))), \
               f"length items_data is not equal {expected_items_count}"

    @staticmethod
    @pytest.mark.parametrize("test_input, expected_response, expected_items_count",
                             [("SELECT * FROM users WHERE username = 'john' OR 'a'='a';-- AND password = ''", 200, 0),
                              ("SELECT * FROM db_table WHERE stud_name = %B;", 200, 0),
                              ("SELECT * FROM users WHERE id=1 ; DELETE FROM users;", 200, 0),
                              ("1234 ' AND 1=0 UNION ALL SELECT 'admin', '81dc9bdb52d04dc20036dbd8313ed055", 200, 0)])
    @pytest.mark.autocomplete
    def test_sql_injections(before_all_fixture, test_input, expected_response, expected_items_count, base_url):
        response = before_all_fixture.get(url=f"{base_url}/{INNER_URL}", params={'search': test_input})
        items_data = response.json()["items"]
        assert response.status_code == expected_response, f"status code is not {expected_response}"
        assert all(list(filter(lambda item: (len(items_data) == expected_items_count), items_data))), \
               f"length items_data is not equal {expected_items_count}"
