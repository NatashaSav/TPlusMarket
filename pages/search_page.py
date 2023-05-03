

class SearchPage:

    @staticmethod
    def get_item_name(items_data, search_phrase):
        for item in items_data:
            item_name = item["name"]
            assert search_phrase in item_name, f"expected to see {item_name} in {item_name}"

    @staticmethod
    def get_products_name(items_data, search_phrase):
        for item in items_data:
            item_name = item["products"][0]["name"]
            assert search_phrase == item_name, f"expected to see {search_phrase}, but received {item_name}"

    @staticmethod
    def get_sorted_list(items_data, general_prices_list, bool_value):
        for item in items_data:
            product_price = item["products"][0]["prices"][0]['price']
            general_prices_list.append(product_price)
        expected_filtered_prices = sorted(general_prices_list, reverse=bool_value)
        assert general_prices_list == expected_filtered_prices, \
               f"expected to see {expected_filtered_prices} but received {general_prices_list}"

    @staticmethod
    def get_separated_items_of_text(items_data, model_name):
        for item in items_data:
            product_name = item["products"][0]["name"]
            separated_items = model_name.split(' ')
            assert (separated_items[0] and separated_items[1] and separated_items[2]) in product_name, \
                   f"expected to see {model_name} in phrase, but received another set of words"

    @staticmethod
    def get_products_filtered_by_brands(items_data, search_phrase, first_brand_name, second_brand_name,
                                        third_brand_name):
        for item in items_data:
            product_name = item["products"][0]["name"]
            assert (search_phrase and first_brand_name) or \
                   (search_phrase and second_brand_name) or \
                   (search_phrase and third_brand_name) in product_name, \
                   f"expected to see {search_phrase} in phrase, but received {product_name}"

    @staticmethod
    def get_products_filtered_by_brands_and_models(items_data, search_phrase, first_brand_name, first_model_name,
                                                   second_brand_name, second_model_name, third_brand_name,
                                                   third_model_name):
        for item in items_data:
            product_name = item["products"][0]["name"]
            assert (search_phrase and first_brand_name and first_model_name) or \
                   (search_phrase and second_brand_name and second_model_name) or \
                   (search_phrase and third_brand_name and third_model_name) in product_name, \
                   f"expected to see {search_phrase} in phrase, but received {product_name}"

    @staticmethod
    def get_products_filtered_by_category(items_data, search_phrase):
        for item in items_data:
            product_name = item["products"][0]["name"]
            assert search_phrase in product_name, f"expected to see {search_phrase} in phrase," \
                                                  f" but received {product_name}"
