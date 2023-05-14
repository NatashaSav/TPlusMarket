import json

import requests

from pages.base_page import BasePage


class RegistrationPage:

    @staticmethod
    def fill_payload_with_data(json_data, cityUuid, email, firstName, lastName, password, phone, surname, verifyCode):
        payload = json_data['PAYLOADS_DATA']['user_registration']
        payload['cityUuid'] = cityUuid
        payload['email'] = email
        payload['firstName'] = firstName
        payload['lastName'] = lastName
        payload['password'] = password
        payload['phone'] = phone
        payload['surname'] = surname
        payload['verifyCode'] = verifyCode
        return payload

    @staticmethod
    def get_response(base_url, INNER_URL, cityUuid, email, firstName, lastName, password, phone, surname, verifyCode):
        my_url = f"{base_url}/{INNER_URL}"
        json_data = BasePage.get_json_file()
        payload = RegistrationPage.fill_payload_with_data(json_data, cityUuid, email, firstName, lastName, password,
                                                          phone, surname, verifyCode)
        header = BasePage.form_header(base_url)
        response = requests.post(url=my_url, headers=header, json=payload)
        return response

    @staticmethod
    def get_content_message(base_url, INNER_URL, cityUuid, email, firstName, lastName, password, phone, surname,
                            verifyCode):
        response = RegistrationPage.get_response(base_url, INNER_URL, cityUuid, email, firstName, lastName, password,
                                                 phone, surname, verifyCode)
        return json.loads(response.content)['message']
