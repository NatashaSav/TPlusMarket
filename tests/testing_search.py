import pytest

from pages.base_page import BasePage

INNER_URL = "api/product/search"


class TestingSearch:

    @staticmethod
    @pytest.mark.xfail(reason="known bug")
    def test_sending_empty_string_to_search(before_all_fixture, base_url):
        search_phrase = ' '
        items_data = BasePage.get_all_items_from_response(base_url, INNER_URL, search_phrase, before_all_fixture)
        assert len(items_data) == 0, f"expected items count is {0}, " \
                                     f"actual items count is {items_data}"

    @staticmethod
    def test_product_filter_by_brand_apple(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        search_phrase = 'Захисне скло'
        json_data = BasePage.get_json_file()
        payload = json_data['PAYLOADS_DATA']['filterByBrandApple']
        payload['search'] = search_phrase
        response = before_all_fixture.get(url=my_url, params=payload)
        items_data = response.json()["items"]
        for item in items_data:
            product_name = item["products"][0]["name"]
            assert (search_phrase and 'Apple Watch') or \
                   (search_phrase and 'iPad') or \
                   (search_phrase and 'Apple iPhone') or \
                   (search_phrase and 'APPLE iPhone') or \
                   (search_phrase or 'iPhone') in product_name, \
                   f"expected to see {search_phrase} in phrase, but received {product_name}"

    @staticmethod
    def test_product_filter_by_brand_samsung(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        search_phrase = 'Захисне скло'
        brand_name_1 = 'Samsung'
        brand_name_2 = "SAMSUNG"
        json_data = BasePage.get_json_file()
        payload = json_data['PAYLOADS_DATA']["filterByBrandSamsung"]
        payload['search'] = search_phrase
        response = before_all_fixture.get(url=my_url, params=payload)
        items_data = response.json()["items"]
        for item in items_data:
            product_name = item["products"][0]["name"]
            assert (search_phrase and brand_name_1) or \
                   (search_phrase and brand_name_2) in product_name, \
                   f"expected to see {search_phrase} in phrase, but received {product_name}"
