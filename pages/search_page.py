class SearchPage:
    @staticmethod
    def get_sorted_list(items_data, general_prices_list, bool_value):
        for item in items_data:
            product_price = item["products"][0]["prices"][0]['price']
            general_prices_list.append(product_price)
        expected_filtered_prices = sorted(general_prices_list, reverse=bool_value)
        return expected_filtered_prices

    @staticmethod
    def get_separated_items_of_text(items_data, model_name):
        for item in items_data:
            product_name = item["products"][0]["name"]
            separated_items = model_name.split(' ')
            return product_name, separated_items
