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
    @pytest.mark.parametrize("search_phrase, expected_items_count", [('fhgjskdnckvj', 0),
                                                                     ('abrakadabra', 0),
                                                                     ('lalala', 0),
                                                                     ('alloha', 0),
                                                                     ('wkdfj', 0),
                                                                     ('+980348', 0),
                                                                     ('-45678', 0),
                                                                     ('+364', 0),
                                                                     (' ', 0)])
    def test_incorrect_and_empty_data(before_all_fixture, search_phrase, expected_items_count, base_url):
        items_data = BasePage.get_all_items_from_response(base_url, INNER_URL, search_phrase, before_all_fixture)
        assert len(items_data) == expected_items_count, f"expected items count is {expected_items_count}, " \
                                                        f"actual items count is {items_data}"

    @staticmethod
    @pytest.mark.parametrize("search_phrase, expected_status_code", [('bluetooth', 401),
                                                                     ('Автомобільний освіжувач повітря', 401),
                                                                     ('Baseus Fabric Artifact Car Fragrance', 401),
                                                                     ('Чохол Cover Samsung Galaxy', 401),
                                                                     ('Чохол Cover Samsung Galaxy S10', 401),
                                                                     ('Samsung Galaxy red', 401),
                                                                     ('Захисне скло', 401),
                                                                     ('Apple Watch 38mm', 401),
                                                                     ('iPhone 14 Plus', 401),
                                                                     ('iPhone 12', 401),
                                                                     ('iPhone 10', 401)])
    def test_check_status_code_of_unauthorized_user(search_phrase, expected_status_code, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        params = {'search': search_phrase}
        response = requests.get(url=my_url, params=params)
        assert response.status_code == expected_status_code
        assert response.reason == 'Unauthorized', f"expected status code is {expected_status_code}," \
                                                  f"actual status code is {response.status_code}"

    @staticmethod
    @pytest.mark.parametrize("test_input, expected_response", [("!@#", 200),
                                                               ("*&%", 200),
                                                               ("(&^)", 200),
                                                               ("+!#", 200),
                                                               ("{@#}", 200),
                                                               ("$#|&", 200),
                                                               ("_)&(", 200),
                                                               ("$%&*", 200)])
    def test_special_symbols(before_all_fixture, test_input, expected_response, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        params = {'search': test_input}
        response = before_all_fixture.get(url=my_url, params=params)
        assert response.status_code == expected_response



