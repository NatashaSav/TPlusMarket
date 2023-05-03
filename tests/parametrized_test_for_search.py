import pytest

from pages.base_page import BasePage
from pages.search_page import SearchPage

INNER_URL = "api/product/search"


class TestParametrizedAutocomplete:

    @staticmethod
    @pytest.mark.parametrize("search_phrase", [('Автомобільний освіжувач повітря'),
                                               ('Автомобільний ос'),
                                               ('освіжувач повітря'),
                                               ('Автомобільний освіжувач повітря Baseus Fabric Artifact Car Fragrance'),
                                               ('Baseus Fabric Artifact Car Fragrance'),
                                               ('освіжувач повітря Baseus')])
    def test_search_phrases(before_all_fixture, search_phrase, base_url):
        items_data = BasePage.get_all_items_from_response(base_url, INNER_URL, search_phrase, before_all_fixture)
        return filter(SearchPage.get_item_name, items_data)

    @staticmethod
    @pytest.mark.parametrize("search_phrase, expected_items_count", [('bor49853fj', 0),
                                                                     ('thresd', 0),
                                                                     ('LaPlAnDiA', 0),
                                                                     ('were_you', 0),
                                                                     ('ghfdnb', 0),
                                                                     ('+384756', 0),
                                                                     ('-67796', 0),
                                                                     ('+098', 0)])
    def test_incorrect_data(before_all_fixture, search_phrase, expected_items_count, base_url):
        items_data = BasePage.get_all_items_from_response(base_url, INNER_URL, search_phrase, before_all_fixture)
        assert len(items_data) == expected_items_count, f"expected items count is {expected_items_count}, " \
                                                        f"actual items count is {items_data}"

    @staticmethod
    @pytest.mark.parametrize("reversed_phrase",
                             [('повітря освіжувач Автомобільний'),
                              ('Fragrance Car Artifact'),
                              ('S10 Чохол Cover'),
                              ('Galaxy red Samsung'),
                              ('Watch 38mm Apple'),
                              ('Plus A730 Galaxy'),
                              ('скло Galaxy Захисне')])
    def test_reversed_words(before_all_fixture, reversed_phrase, base_url):
        items_data = BasePage.get_all_items_from_response(base_url, INNER_URL, reversed_phrase, before_all_fixture)
        item_name = items_data[0]['name']
        reversed_item = reversed_phrase.split(' ')
        assert (reversed_item[0] and reversed_item[1] and reversed_item[2]) in item_name, \
            f"expected to see {reversed_phrase} in actual phrase {item_name}"

    @staticmethod
    @pytest.mark.parametrize("search_phrase",
                            [('Автомобільний освіжувач повітря Baseus Circle Vehicle Fragrance silver'),
                             ('holder sim card Apple iPad Pro 9.7 2016 gold'),
                             ('Camera glass Apple iPhone 11 Pro with frame gold (Original)'),
                             ('Charge connector Asus Z500M ZenPad 3S (Type-C)'),
                             ('Жало 900M-T-5C усічений циліндр, 5мм')])
    def test_phrase_recognition_by_the_full_sentences_with_color_name(before_all_fixture, search_phrase, base_url):
        items_data = BasePage.get_all_items_from_response(base_url, INNER_URL, search_phrase, before_all_fixture)
        return filter(SearchPage.get_products_name, items_data)

    @staticmethod
    @pytest.mark.parametrize("abbreviation, expected_phrase",
                             [('B F Ar Car Fr',
                               'Автомобільний освіжувач повітря Baseus Fabric Artifact Car Fragrance'),
                              ('Ba YI M30 1.5', 'Audio кабель AUX 3.5mm Baseus Yiven M30 1.5m'),
                              ('Ко ме Ne ST', 'Комутатор мережевий Netis ST3108S'),
                              ('US H ad Ba Ha 5 in 1', 'USB HUB adapter Baseus Harmonica 5 in 1'),
                              ('D D HD 2TB Bl', 'Жорсткий диск 2.5 HDD ADATA USB 3.2 Gen.'
                                                ' 1 DashDrive Durable HD680 2TB Black')])
    def test_phrase_recognition_by_abbreviation_words(before_all_fixture, abbreviation, expected_phrase, base_url):
        items_data = BasePage.get_all_items_from_response(base_url, INNER_URL, abbreviation, before_all_fixture)
        actual_phrase = items_data[0]['name']
        assert actual_phrase == expected_phrase, f"expected to see {expected_phrase}, bur received {actual_phrase}"

    @staticmethod
    @pytest.mark.parametrize("article_name, full_phrase", [
                            ('00-00053339', 'Автомобільний освіжувач повітря Baseus Fabric Artifact Car Fragrance'),
                            ('00-00091512', 'Press-button Home Huawei MediaPad M5 Lite 10 black'),
                            ('00-00013899', 'IC CPU MSM8916 5VV'),
                            ('00-00100331', 'IC Light control ELC180 (TPS62180) (Original)')])
    def test_phrase_recognition_by_article_name(before_all_fixture, article_name, full_phrase, base_url):
        items_data = BasePage.get_all_items_from_response(base_url, INNER_URL, article_name, before_all_fixture)
        return filter(SearchPage.get_item_name, items_data)

    @staticmethod
    @pytest.mark.parametrize("model_name", [('Чохол Cover Samsung Galaxy'),
                                            ('Набір металевих пластин для Apple iPhone 13'),
                                            ('Верхня панель кришки Google Pixel'),
                                            ('Charge connector DC')])
    def test_product_filtering_from_cheaper_to_more_expensive(before_all_fixture, model_name, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        json_data = BasePage.get_json_file()
        payload = json_data['PAYLOADS_DATA']['orderByASCPrice']
        payload['search'] = model_name
        general_prices_list = []
        response = before_all_fixture.get(url=my_url, params=payload)
        items_data = response.json()["items"]
        return filter(SearchPage.get_sorted_list(items_data, general_prices_list, bool_value=False), items_data)

    @staticmethod
    @pytest.mark.parametrize("model_name", [('Чохол Cover Samsung Galaxy S10'),
                                            ('Hands free connector Huawei'),
                                            ('Flat cable універсальний'),
                                            ('Battery Prime iPad')])
    def test_product_filtering_from_more_expensive_to_cheaper(before_all_fixture, model_name, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        json_data = BasePage.get_json_file()
        payload = json_data['PAYLOADS_DATA']['orderByDESCPrice']
        payload['search'] = model_name
        general_prices_list = []
        response = before_all_fixture.get(url=my_url, params=payload)
        items_data = response.json()["items"]
        return filter(SearchPage.get_sorted_list(items_data, general_prices_list, bool_value=True), items_data)

    @staticmethod
    @pytest.mark.parametrize("model_name", [('Samsung Galaxy red'),
                                            ('Xiaomi 11T black'),
                                            ('Захисна плівка Realme'),
                                            ('Набір гвинтів iPhone'),
                                            ('Клей Mechanic червоний')])
    def test_best_phrase_coincidence(before_all_fixture, model_name, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        json_data = BasePage.get_json_file()
        payload = json_data['PAYLOADS_DATA']['orderByDESCRank']
        payload['search'] = model_name
        response = before_all_fixture.get(url=my_url, params=payload)
        items_data = response.json()["items"]
        return filter(SearchPage.get_separated_items_of_text, items_data)

    @staticmethod
    @pytest.mark.parametrize("model_name, brand_name, expected_result", [('17', '2680', 'Apple Watch 38mm'),
                                                                         ('17', '851', 'iPhone 14 Plus'),
                                                                         ('178', '296', 'A730 Galaxy A8 Plus'),
                                                                         ('178', '231', 'A500 Galaxy A5')])
    def test_product_filter_by_brand_and_model_name(before_all_fixture, model_name, brand_name, expected_result,
                                                    base_url):
        my_url = f"{base_url}/{INNER_URL}"
        search_phrase = 'Захисне скло'
        json_data = BasePage.get_json_file()
        payload = json_data['PAYLOADS_DATA']['filterByBrandAndModel']
        payload['search'] = search_phrase
        payload['brandIds[0]'] = model_name
        payload['modelIds[0]'] = brand_name
        response = before_all_fixture.get(url=my_url, params=payload)
        items_data = response.json()["items"]
        product_name_list = [item["products"][0]["name"] for item in items_data]
        for product_name in product_name_list:
            assert (search_phrase and expected_result) in product_name, \
                   f"expected to see {search_phrase} and {expected_result} in phrase, but received {product_name}"

    @staticmethod
    @pytest.mark.parametrize("first_brand_id, first_brand_name, second_brand_id, second_brand_name",
                                                                [('123', 'Lenovo', '138', 'Meizu'),
                                                                 ('54', 'Doogee', '20', 'Asus')])
    def test_product_filter_by_two_brands(before_all_fixture, first_brand_id, first_brand_name, second_brand_id,
                                          second_brand_name, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        search_phrase = 'Захисне скло'
        json_data = BasePage.get_json_file()
        payload = json_data['PAYLOADS_DATA']['filterByTwoBrands']
        payload['search'] = search_phrase
        payload['brandIds[0]'] = first_brand_id
        payload['brandIds[1]'] = second_brand_id
        response = before_all_fixture.get(url=my_url, params=payload)
        items_data = response.json()["items"]
        product_name_list = [item["products"][0]["name"] for item in items_data]
        for product_name in product_name_list:
            assert (search_phrase and first_brand_name) or \
                   (search_phrase and second_brand_name) in product_name, \
                   f"expected to see {search_phrase} in phrase, but received {product_name}"

    @staticmethod
    @pytest.mark.parametrize("first_brand_id, first_brand_name, first_model_id, first_model_name, \
                             second_brand_id, second_brand_name, second_model_id, second_model_name",
                             [('123', 'Lenovo', '2654', 'Lenovo Yoga Tablet 2-830',
                               '138', 'Meizu', '12', 'Meizu 16')])
    def test_product_filter_by_two_brands_and_two_models(before_all_fixture, first_brand_id, first_brand_name,
                                                         first_model_id, first_model_name,
                                                         second_brand_id, second_brand_name,
                                                         second_model_id, second_model_name, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        search_phrase = 'Захисне скло'
        json_data = BasePage.get_json_file()
        payload = json_data['PAYLOADS_DATA']['filterBy2BrandsAnd2Models']
        payload['search'] = search_phrase
        payload['brandIds[0]'] = first_brand_id
        payload['brandIds[1]'] = second_brand_id
        payload['modelIds[0]'] = first_model_id
        payload['modelIds[1]'] = second_model_id
        response = before_all_fixture.get(url=my_url, params=payload)
        items_data = response.json()["items"]
        product_name_list = [item["products"][0]["name"] for item in items_data]
        for product_name in product_name_list:
            assert (search_phrase and first_brand_name and first_model_name) or \
                   (search_phrase and second_brand_name and second_model_name) in product_name, \
                   f"expected to see {search_phrase} in phrase, but received {product_name}"

    @staticmethod
    @pytest.mark.parametrize("first_brand_id, first_brand_name, second_brand_id, second_brand_name, "
                             "third_brand_id, third_brand_name",
                             [('247', 'Sony', '20', 'Asus', '188', 'ZTE')])
    def test_product_filter_by_three_brands(before_all_fixture, first_brand_id, first_brand_name, second_brand_id,
                                            second_brand_name, third_brand_id, third_brand_name, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        search_phrase = 'Захисне скло'
        json_data = BasePage.get_json_file()
        payload = json_data['PAYLOADS_DATA']['filterByThreeBrands']
        payload['search'] = search_phrase
        payload['brandIds[0]'] = first_brand_id
        payload['brandIds[1]'] = second_brand_id
        payload['brandIds[2]'] = third_brand_id
        response = before_all_fixture.get(url=my_url, params=payload)
        items_data = response.json()["items"]
        return filter(SearchPage.get_products_filtered_by_brands, items_data)

    @staticmethod
    @pytest.mark.parametrize("first_brand_id, first_brand_name, first_model_id, first_model_name, \
                              second_brand_id, second_brand_name, second_model_id, second_model_name, "
                             "third_brand_id, third_brand_name, third_model_id, third_model_name",
                             [('247', 'Sony', '2099', 'D2302 Xperia M2',
                               '20', 'Asus', '531', 'ZenPad 10',
                               '188', 'ZTE', '2843', 'Blade 20 Smart')])
    def test_product_filter_by_three_brands_and_three_models(before_all_fixture, first_brand_id, first_brand_name,
                                                             first_model_id, first_model_name, second_brand_id,
                                                             second_brand_name, second_model_id, second_model_name,
                                                             third_brand_id, third_brand_name, third_model_id,
                                                             third_model_name, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        search_phrase = 'Захисне скло'
        json_data = BasePage.get_json_file()
        payload = json_data['PAYLOADS_DATA']['filterBy2BrandsAnd2Models']
        payload['search'] = search_phrase
        payload['brandIds[0]'] = first_brand_id
        payload['brandIds[1]'] = second_brand_id
        payload['brandIds[2]'] = third_brand_id
        payload['modelIds[0]'] = first_model_id
        payload['modelIds[1]'] = second_model_id
        payload['modelIds[2]'] = third_model_id
        response = before_all_fixture.get(url=my_url, params=payload)
        items_data = response.json()["items"]
        return filter(SearchPage.get_products_filtered_by_brands_and_models, items_data)

    @staticmethod
    @pytest.mark.parametrize("search_phrase, category_id",
                             [('Комплект бічних кнопок корпусу', '757'),
                              ('Автомобільний органайзер', '13'),
                              ('Струмопровідний лак', '9'),
                              ('2D Трафарет QianLi Black', '10'),
                              ('Захисна TPU плівка іЗі', '13'),
                              ('Мікросхема Realtek', '213'),
                              ('Автотримач Baseus Smart', '753'),
                              ('Заміна підсвітки', '188'),
                              ('Battery GP Lithium', '328'),
                              ('BGA кульки', '160')])
    def test_product_filter_by_category(before_all_fixture, category_id, search_phrase, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        json_data = BasePage.get_json_file()
        payload = json_data['PAYLOADS_DATA']['filterByCategory']
        payload['search'] = search_phrase
        payload['categoryId'] = category_id
        response = before_all_fixture.get(url=my_url, params=payload)
        items_data = response.json()["items"]
        return filter(SearchPage.get_products_filtered_by_category, items_data)
