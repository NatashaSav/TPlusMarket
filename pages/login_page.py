import requests

from pages.base_page import BasePage


class LoginPage:

    @staticmethod
    def get_response_data(base_url, INNER_URL, email, password):
        my_url = f"{base_url}/{INNER_URL}"
        json_data = BasePage.get_json_file()
        payload = json_data['PAYLOADS_DATA']['user_login']
        payload['email'] = email
        payload['password'] = password
        header = BasePage.form_header(base_url)
        response = requests.post(url=my_url, headers=header, json=payload)
        return response
