import pytest

INNER_URL = "api/product/search"


class TestingSearch:

    @staticmethod
    def test_sending_incorrect_string_to_search(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        params = {'search': 'fhgjskdnckvj'}
        response = before_all_fixture.get(url=my_url, params=params)
        items_data = len(response.json()["items"])
        expected_items_count = 0
        assert items_data == expected_items_count, f"expected items count is {expected_items_count}, " \
                                                   f"actual items count is {items_data}"

    @staticmethod
    def test_sending_correct_string_to_search(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        search_phrase = 'Автомобільний освіжувач повітря'
        params = {'search': search_phrase}
        response = before_all_fixture.get(url=my_url, params=params)
        items_data = response.json()["items"]
        for item in items_data:
            item_name = item["name"]
            assert search_phrase in item_name, f"expected to see {search_phrase} in {item_name}"

    @pytest.mark.xfail(reason="known bug")
    def test_sending_empty_string_to_search(self, before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        params = {'search': ' '}
        response = before_all_fixture.get(url=my_url, params=params)
        items_data = len(response.json()["items"])
        expected_items_count = 0
        assert items_data == expected_items_count, f"expected items count is {expected_items_count}, " \
                                                   f"actual items count is {items_data}"

    @staticmethod
    def test_phrase_recognition_by_the_first_search_words(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        part_of_phrase = 'Автомобільний освіжувач повітря'
        search_words = 'Автомобільний ос'
        params = {'search': search_words}
        response = before_all_fixture.get(url=my_url, params=params)
        items_data = response.json()["items"]
        for item in items_data:
            item_name = item["name"]
            assert part_of_phrase in item_name, f"expected to see {search_words} in actual phrase {item_name}"

    @staticmethod
    def test_phrase_recognition_by_the_few_search_words(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        part_of_phrase = 'Автомобільний освіжувач повітря'
        search_words = 'освіжувач повітря'
        params = {'search': search_words}
        response = before_all_fixture.get(url=my_url, params=params)
        items_data = response.json()["items"]
        for item in items_data:
            item_name = item["name"]
            assert part_of_phrase in item_name, f"expected to see {part_of_phrase} in actual phrase {item_name}"

    @staticmethod
    def test_phrase_recognition_by_the_full_sentences_with_color_name(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        full_phrase = 'Автомобільний освіжувач повітря Baseus Circle Vehicle Fragrance silver'
        params = {'search': full_phrase}
        response = before_all_fixture.get(url=my_url, params=params)
        items_data = response.json()["items"]
        for item in items_data:
            item_name = item["products"][0]["name"]
            assert full_phrase in item_name, f"expected to see {full_phrase} in actual phrase {item_name}"

    @staticmethod
    def test_phrase_recognition_by_the_full_sentences(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        full_phrase = 'Автомобільний освіжувач повітря Baseus Fabric Artifact Car Fragrance'
        params = {'search': full_phrase}
        response = before_all_fixture.get(url=my_url, params=params)
        items_data = response.json()["items"]
        for item in items_data:
            item_name = item["name"]
            assert full_phrase in item_name, f"expected to see {full_phrase} in actual phrase {item_name}"

    @staticmethod
    def test_phrase_recognition_by_the_english_product_name(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        part_of_phrase = 'Baseus Fabric Artifact Car Fragrance'
        params = {'search': part_of_phrase}
        response = before_all_fixture.get(url=my_url, params=params)
        items_data = response.json()["items"]
        for item in items_data:
            item_name = item["name"]
            assert part_of_phrase in item_name, f"expected to see {part_of_phrase} in actual phrase {item_name}"

    @staticmethod
    def test_phrase_recognition_by_abbreviation_words(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        full_phrase = 'Автомобільний освіжувач повітря Baseus Fabric Artifact Car Fragrance'
        abbreviation = 'B F Ar Car Fr'
        params = {'search': abbreviation}
        response = before_all_fixture.get(url=my_url, params=params)
        items_data = response.json()["items"]
        for item in items_data:
            item_name = item["name"]
            assert full_phrase in item_name, f"expected to see {full_phrase} in actual phrase {item_name}"

    @staticmethod
    def test_phrase_recognition_where_words_are_reversed(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        full_phrase = 'Автомобільний освіжувач повітря Baseus Fabric Artifact Car Fragrance'
        reversed_words = 'Fragrance Car Fabric Baseus'
        params = {'search': reversed_words}
        response = before_all_fixture.get(url=my_url, params=params)
        items_data = response.json()["items"]
        for item in items_data:
            item_name = item["name"]
            assert full_phrase in item_name, f"expected to see {full_phrase} in actual phrase {item_name}"

    @staticmethod
    def test_phrase_recognition_by_article_name(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        full_phrase = 'Автомобільний освіжувач повітря Baseus Fabric Artifact Car Fragrance'
        article_name = '00-00053339'
        params = {'search': article_name}
        response = before_all_fixture.get(url=my_url, params=params)
        items_data = response.json()["items"]
        for item in items_data:
            item_name = item["name"]
            assert full_phrase in item_name, f"expected to see {full_phrase} in actual phrase {item_name}"

    @staticmethod
    def test_product_filtering_from_cheaper_to_more_expensive(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        model_name = 'Чохол Cover Samsung Galaxy'
        general_prices_list = []
        payload = {'search': model_name,
                   'favorite': 'false',
                   'limit': 25,
                   'page': 2,
                   'orderBy[price]': 'ASC',
                   'receipt': 'false',
                   'onlyTplus': 'true'}
        response = before_all_fixture.get(url=my_url, params=payload)
        items_data = response.json()["items"]
        for item in items_data:
            product_price = item["products"][0]["prices"][0]['price']
            general_prices_list.append(product_price)
        expected_filtered_prices = sorted(general_prices_list)
        assert general_prices_list == expected_filtered_prices,\
            f"expected to see {expected_filtered_prices} but received {general_prices_list}"

    @staticmethod
    def test_product_filtering_from_more_expensive_to_cheaper(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        model_name = 'Чохол Cover Samsung Galaxy S10'
        general_prices_list = []
        payload = {'search': model_name,
                   'favorite': 'false',
                   'limit': 24,
                   'page': 1,
                   'orderBy[price]': 'DESC',
                   'receipt': 'false',
                   'onlyTplus': 'true'}
        response = before_all_fixture.get(url=my_url, params=payload)
        items_data = response.json()["items"]
        for item in items_data:
            product_price = item["products"][0]["prices"][0]['price']
            general_prices_list.append(product_price)
        expected_filtered_prices = sorted(general_prices_list, reverse=True)
        assert general_prices_list == expected_filtered_prices,\
            f"expected to see {expected_filtered_prices} but received {general_prices_list}"

    @staticmethod
    def test_best_phrase_coincidence(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        model_name = 'Samsung Galaxy red'
        payload = {'search': model_name,
                   'favorite': 'false',
                   'limit': 24,
                   'page': 1,
                   'orderBy[rank]': 'DESC',
                   'receipt': 'false',
                   'onlyTplus': 'true'}
        response = before_all_fixture.get(url=my_url, params=payload)
        items_data = response.json()["items"]
        for item in items_data:
            product_name = item["products"][0]["name"]
            assert 'Samsung' and 'Galaxy' and 'red' in product_name, \
                   f"expected to see {model_name} in phrase, but received another set of words"

    @staticmethod
    def test_product_filter_by_brand_apple(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        search_phrase = 'Захисне скло'
        payload = {'search': search_phrase,
                   'favorite': 'false',
                   'brandIds[0]': 17,
                   'limit': 24,
                   'page': 1,
                   'receipt': 'false'}
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
    def test_product_filter_by_brand_apple_and_model_apple_watch_38mm(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        search_phrase = 'Захисне скло'
        model_name = 'Apple Watch 38mm'
        payload = {'search': search_phrase,
                   'favorite': 'false',
                   'brandIds[0]': 17,
                   'modelIds[0]': 2680,
                   'limit': 24,
                   'page': 1,
                   'receipt': 'false'}
        response = before_all_fixture.get(url=my_url, params=payload)
        items_data = response.json()["items"]
        for item in items_data:
            product_name = item["products"][0]["name"]
            assert (search_phrase and model_name) in product_name, \
                f"expected to see {search_phrase} and {model_name} in phrase, but received {product_name}"

    @staticmethod
    def test_product_filter_by_brand_apple_and_model_iphone_14_plus(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        search_phrase = 'Захисне скло'
        model_name = 'iPhone 14 Plus'
        payload = {'search': search_phrase,
                   'favorite': 'false',
                   'brandIds[0]': 17,
                   'modelIds[0]': 851,
                   'limit': 24,
                   'page': 1,
                   'receipt': 'false'}
        response = before_all_fixture.get(url=my_url, params=payload)
        items_data = response.json()["items"]
        for item in items_data:
            product_name = item["products"][0]["name"]
            assert (search_phrase and model_name) in product_name, \
                f"expected to see {search_phrase} and {model_name} in phrase, but received {product_name}"

    @staticmethod
    def test_product_filter_by_brand_samsung(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        search_phrase = 'Захисне скло'
        brand_name_1 = 'Samsung'
        brand_name_2 = "SAMSUNG"
        payload = {'search': search_phrase,
                   'favorite': 'false',
                   'brandIds[0]': 178,
                   'limit': 24,
                   'page': 1,
                   'receipt': 'false'}
        response = before_all_fixture.get(url=my_url, params=payload)
        items_data = response.json()["items"]
        for item in items_data:
            product_name = item["products"][0]["name"]
            assert (search_phrase and brand_name_1) or \
                   (search_phrase and brand_name_2) in product_name, \
                   f"expected to see {search_phrase} in phrase, but received {product_name}"

    @staticmethod
    def test_product_filter_by_brand_samsung_and_model_a730_galaxy_a8(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        search_phrase = 'Захисне скло'
        brand_name = 'A730 Galaxy A8 Plus'
        payload = {'search': search_phrase,
                   'favorite': 'false',
                   'brandIds[0]': 178,
                   'modelIds[0]': 296,
                   'limit': 24,
                   'page': 1,
                   'receipt': 'false'}
        response = before_all_fixture.get(url=my_url, params=payload)
        items_data = response.json()["items"]
        for item in items_data:
            product_name = item["products"][0]["name"]
            assert (search_phrase and brand_name) and ('Samsung' or 'SAMSUNG') or \
                   (search_phrase and brand_name) and ('Samsung' or 'SAMSUNG') in product_name, \
                   f"expected to see {search_phrase} in phrase, but received {product_name}"

    @staticmethod
    def test_product_filter_by_brand_samsung_and_model_a500_galaxy_a5(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        search_phrase = 'Захисне скло'
        brand_name = 'A500 Galaxy A5'
        payload = {'search': search_phrase,
                   'favorite': 'false',
                   'brandIds': 178,
                   'modelIds': 231,
                   'limit': 24,
                   'page': 1,
                   'receipt': 'false'}
        response = before_all_fixture.get(url=my_url, params=payload)
        items_data = response.json()["items"]
        for item in items_data:
            product_name = item["products"][0]["name"]
            assert (search_phrase and brand_name) and ('Samsung' or 'SAMSUNG') in product_name, \
                   f"expected to see {search_phrase} in phrase, but received {product_name}"

    @staticmethod
    def test_product_filter_by_two_brands(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        search_phrase = 'Захисне скло'
        first_brand_name = 'Lenovo'
        second_brand_name = 'Meizu'
        payload = {'search': search_phrase,
                   'favorite': 'false',
                   'brandIds[0]': 123,
                   'brandIds[1]': 138,
                   'limit': 24,
                   'page': 1,
                   'receipt': 'false'}
        response = before_all_fixture.get(url=my_url, params=payload)
        items_data = response.json()["items"]
        for item in items_data:
            product_name = item["products"][0]["name"]
            assert (search_phrase and first_brand_name) or \
                   (search_phrase and second_brand_name) in product_name, \
                   f"expected to see {search_phrase} in phrase, but received {product_name}"

    @staticmethod
    def test_product_filter_by_two_brands_and_two_models(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        search_phrase = 'Захисне скло'
        first_brand_name = 'Lenovo'
        second_brand_name = 'Meizu'
        first_model_name = 'Lenovo Yoga Tablet 2-830'
        second_model_name = 'Lenovo Yoga Tablet B8000'
        third_model_name = 'Meizu 16'
        payload = {'search': search_phrase,
                   'favorite': 'false',
                   'brandIds[0]': 123,
                   'brandIds[1]': 138,
                   'modelIds[0]': 12,
                   'modelIds[1]': 2654,
                   'modelIds[2]': 2656,
                   'limit': 24,
                   'page': 1,
                   'receipt': 'false'}
        response = before_all_fixture.get(url=my_url, params=payload)
        items_data = response.json()["items"]
        for item in items_data:
            product_name = item["products"][0]["name"]
            assert (search_phrase and first_brand_name and first_model_name) or \
                   (search_phrase and first_brand_name and second_model_name) or \
                   (search_phrase and second_brand_name and third_model_name) in product_name, \
                   f"expected to see {search_phrase} in phrase, but received {product_name}"

    @staticmethod
    def test_product_filter_by_three_brands(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        search_phrase = 'Захисне скло'
        first_brand_name = 'Sony'
        second_brand_name = 'Asus'
        third_brand_name = 'ZTE'
        payload = {'search': search_phrase,
                   'favorite': 'false',
                   'brandIds[0]': 247,
                   'brandIds[1]': 20,
                   'brandIds[2]': 188,
                   'limit': 36,
                   'page': 3,
                   'receipt': 'false'}
        response = before_all_fixture.get(url=my_url, params=payload)
        items_data = response.json()["items"]
        for item in items_data:
            product_name = item["products"][0]["name"]
            assert (search_phrase and first_brand_name) or \
                   (search_phrase and second_brand_name) or \
                   (search_phrase and third_brand_name) in product_name, \
                   f"expected to see {search_phrase} in phrase, but received {product_name}"

    @staticmethod
    def test_product_filter_by_three_brands_and_three_models(before_all_fixture, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        search_phrase = 'Захисне скло'
        first_brand_name = 'Sony'
        second_brand_name = 'Asus'
        third_brand_name = 'ZTE'
        first_model_name = 'D2302 Xperia M2'
        second_model_name = 'ZenPad 10'
        third_model_name = 'Blade 20 Smart'
        payload = {'search': search_phrase,
                   'favorite': 'false',
                   'brandIds[0]': 247,
                   'brandIds[1]': 20,
                   'brandIds[2]': 188,
                   'modelIds[0]': 2099,
                   'modelIds[1]': 531,
                   'modelIds[2]': 2843,
                   'limit': 24,
                   'page': 1,
                   'receipt': 'false'}
        response = before_all_fixture.get(url=my_url, params=payload)
        items_data = response.json()["items"]
        for item in items_data:
            product_name = item["products"][0]["name"]
            assert (search_phrase and first_brand_name and first_model_name) or \
                   (search_phrase and second_brand_name and second_model_name) or \
                   (search_phrase and third_brand_name and third_model_name) in product_name, \
                   f"expected to see {search_phrase} in phrase, but received {product_name}"
