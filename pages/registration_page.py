import json

import requests

from pages.base_page import BasePage


class RegistrationPage:

    @staticmethod
    def fill_payload_with_data(json_data, cityUuid, email, firstName, lastName, password, phone, surname):
        payload = json_data['PAYLOADS_DATA']['user_registration']
        payload['cityUuid'] = cityUuid
        payload['email'] = email
        payload['firstName'] = firstName
        payload['lastName'] = lastName
        payload['password'] = password
        payload['phone'] = phone
        payload['surname'] = surname
        return payload

    @staticmethod
    def get_response(base_url, INNER_URL, cityUuid, email, firstName, lastName, password, phone, surname):
        my_url = f"{base_url}/{INNER_URL}"
        json_data = BasePage.get_json_file()
        payload = RegistrationPage.fill_payload_with_data(json_data, cityUuid, email, firstName, lastName, password,
                                                          phone, surname)
        header = BasePage.form_header(base_url)
        response = requests.post(url=my_url, headers=header, json=payload)
        return response

    @staticmethod
    def get_extended_response(base_url, INNER_URL, response, verification_code):
        my_url = f"{base_url}/{INNER_URL}"
        header = BasePage.form_header(base_url)
        payload = json.loads(response.request.body)
        payload['verifyCode'] = verification_code
        return requests.post(url=my_url, headers=header, json=payload)

    @staticmethod
    def get_content_message_with_extended_payload(base_url, INNER_URL, response, verification_code):
        response = RegistrationPage.get_extended_response(base_url, INNER_URL, response, verification_code)
        return json.loads(response.content)['message']
