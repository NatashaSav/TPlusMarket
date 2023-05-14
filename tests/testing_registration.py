import pytest
import requests
import json

from pages.base_page import BasePage
from pages.registration_page import RegistrationPage

INNER_URL = "api/auth/sign-up"


class TestingRegistration:

    @staticmethod
    @pytest.mark.parametrize("cityUuid, email, firstName, lastName, password, phone, surname, expected_status_code",
                             [('1b009444-4e4a-11ed-a361-48df37b92096', 'kristina_osadcha@gmail.com',
                               'Kristina', 'Osadcha', 'QWD564vf', '380964903845', 'Vladimirovna', 200),
                              ('d30282f8-feee-11e9-91ff-0025b501a04b', 'marina_levchenko@gmail.com',
                               'Marina', 'Levchenko', 'BGKF122kj', '380936912376', 'Olegovna', 200)])
    def test_successful_user_status_code(cityUuid, email, firstName, lastName, password, phone,
                                         surname, expected_status_code, base_url):
        my_url = f"{base_url}/{INNER_URL}"
        json_data = BasePage.get_json_file()
        payload = json_data['PAYLOADS_DATA']['user_registration']
        payload['cityUuid'] = cityUuid
        payload['email'] = email
        payload['firstName'] = firstName
        payload['lastName'] = lastName
        payload['password'] = password
        payload['phone'] = phone
        payload['surname'] = surname
        header = BasePage.form_header(base_url)
        response = requests.post(url=my_url, headers=header, json=payload)
        assert response.status_code == expected_status_code

    @staticmethod
    @pytest.mark.parametrize("cityUuid, email, firstName, lastName, password, phone, surname, verifyCode, "
                             "expected_status_code, expected_message",
                             [('', 'kristina_osadcha@gmail.com', 'Kristina', 'Osadcha', 'QWD564vf', '380964903845',
                               'Vladimirovna', '5691', 400, 'cityUuid should not be empty'),
                              ('1b009444-4e4a-11ed-a361-48df37b92096', '', 'Kristina', 'Osadcha', 'QWD564vf',
                               '380964903845', 'Vladimirovna', '5691', 400, 'email must be longer than or equal to'
                                                                       ' 6 characters'),
                              ('1b009444-4e4a-11ed-a361-48df37b92096', 'kristina_osadcha@gmail.com', '', 'Osadcha',
                               'QWD564v', '380964903845', 'Vladimirovna', '5691', 400, 'firstName should not be empty'),
                              ('1b009444-4e4a-11ed-a361-48df37b92096', 'kristina_osadcha@gmail.com', 'Kristina',
                               '', 'QWD564vf', '380964903845', 'Vladimirovna', '5691', 400,
                               'lastName should not be empty'),
                              ('1b009444-4e4a-11ed-a361-48df37b92096', 'kristina_osadcha@gmail.com', 'Kristina',
                               'Osadcha', '', '380964903845', 'Vladimirovna', '5691', 400,
                               'password should not be empty'),
                              ('1b009444-4e4a-11ed-a361-48df37b92096', 'kristina_osadcha@gmail.com', 'Kristina',
                               'Osadcha', 'QWD564vf', '', 'Vladimirovna', '5691', 400, 'phone should not be empty'),
                              ('1b009444-4e4a-11ed-a361-48df37b92096', 'kristina_osadcha@gmail.com', 'Kristina',
                               'Osadcha', 'QWD564vf', '380964903845', '', '5691', 400, 'surname should not be empty'),
                              ('1b009444-4e4a-11ed-a361-48df37b92096', 'kristina_osadcha@gmail.com', 'Kristina',
                               'Osadcha', 'QWD564vf', '380964903845', 'Vladimirovna', '58795', 400,
                               'verifyCode must be shorter than or equal to 4 characters')])
    def test_registration_user_with_empty_field(before_all_fixture, cityUuid, email, firstName, lastName, password,
                                                phone, surname, verifyCode, expected_status_code, expected_message,
                                                base_url):
        response = RegistrationPage.get_response(base_url, INNER_URL, cityUuid, email, firstName,
                                                 lastName, password, phone, surname, verifyCode)
        content_msg = RegistrationPage.get_content_message(base_url, INNER_URL, cityUuid, email, firstName, lastName,
                                                           password, phone, surname, verifyCode)
        assert response.status_code == expected_status_code and expected_message in content_msg.values()

    @staticmethod
    @pytest.mark.parametrize("cityUuid, email, firstName, lastName, password, phone, surname, verifyCode, "
                             "expected_status_code, expected_message",
                             [('1b009444-4e4a-11ed-a361-48df37b92096', 'kristina_osadcha@gmail.com',
                               'Kristina', 'Osadcha', 'QWD564vf', '380964903845', 'Vladimirovna', '5891', 400,
                               'Invalid verification code'),
                              ('1b009444-4e4a-11ed-a361-48df37b92096', 'kristina_osadcha@gmail.com',
                               'Kristina', 'Osadcha', 'QWD564vf', '380964903845', 'Vladimirovna', '9857', 400,
                               'Invalid verification code')
                              ])
    def test_invalid_verification_code(before_all_fixture, cityUuid, email, firstName, lastName, password, phone,
                                         surname, verifyCode, expected_status_code, expected_message, base_url):
        response = RegistrationPage.get_response(base_url, INNER_URL, cityUuid, email, firstName,
                                                 lastName, password, phone, surname, verifyCode)
        content_msg = RegistrationPage.get_content_message(base_url, INNER_URL, cityUuid, email, firstName, lastName,
                                                           password, phone, surname, verifyCode)
        assert response.status_code == expected_status_code and expected_message in content_msg.values()

    @staticmethod
    @pytest.mark.parametrize("cityUuid, email, firstName, lastName, password, phone, surname, verifyCode, "
                             "expected_status_code, expected_message",
                             [('1b009444-4e4a-11ed-a361-48df37b92096', 'kristina_osadcha@gmail.com',
                               'K', 'Osadcha', 'QWD564vf', '380964903845', 'Vladimirovna', "", 400,
                               'firstName must be longer than or equal to 2 characters'),
                              ('d30282f8-feee-11e9-91ff-0025b501a04b', 'marina_levchenko@gmail.com',
                               'M', 'Levchenko', 'BGKF122kj', '380936912376', 'Olegovna', "", 400,
                               'firstName must be longer than or equal to 2 characters')])
    def test_msg_when_first_name_is_too_short(cityUuid, email, firstName, lastName, password, phone,
                                         surname, verifyCode, expected_status_code, expected_message, base_url):
        response = RegistrationPage.get_response(base_url, INNER_URL, cityUuid, email, firstName,
                                                 lastName, password, phone, surname, verifyCode)
        content_msg = RegistrationPage.get_content_message(base_url, INNER_URL, cityUuid, email, firstName, lastName,
                                                           password, phone, surname, verifyCode)
        assert response.status_code == expected_status_code and expected_message in content_msg.values()


    @staticmethod
    @pytest.mark.parametrize("cityUuid, email, firstName, lastName, password, phone, surname, verifyCode,"
                             "expected_status_code, expected_message",
                             [('1b009444-4e4a-11ed-a361-48df37b92096', 'kristina_osadcha@gmail.com',
                               'Kristiiiiiiiiiiiiiiiiiiiiinnnnnnnnnnaaa', 'Osadcha', 'QWD564vf', '380964903845',
                               'Vladimirovna', "", 400, 'firstName must be shorter than or equal to 30 characters'),
                              ('d30282f8-feee-11e9-91ff-0025b501a04b', 'marina_levchenko@gmail.com',
                               'Maaaaaaarrriiinnnnnnnnnnnnnnnnaaaaaaaaa', 'Levchenko', 'BGKF122kj', '380936912376',
                               'Olegovna', "", 400, 'firstName must be shorter than or equal to 30 characters')])
    def test_msg_when_first_name_is_too_long(cityUuid, email, firstName, lastName, password, phone,
                                         surname, verifyCode, expected_status_code, expected_message, base_url):
        response = RegistrationPage.get_response(base_url, INNER_URL, cityUuid, email, firstName,
                                                 lastName, password, phone, surname, verifyCode)
        content_msg = RegistrationPage.get_content_message(base_url, INNER_URL, cityUuid, email, firstName, lastName,
                                                           password, phone, surname, verifyCode)
        assert response.status_code == expected_status_code and expected_message in content_msg.values()

    @staticmethod
    @pytest.mark.parametrize("cityUuid, email, firstName, lastName, password, phone, surname, verifyCode,"
                             "expected_status_code, expected_message",
                             [('1b009444-4e4a-11ed-a361-48df37b92096', 'kristina_osadcha@gmail.com',
                               'Kristina', 'O', 'QWD564vf', '380964903845', 'Vladimirovna', "", 400, 'lastName must be'
                                                                            ' longer than or equal to 2 characters'),
                              ('d30282f8-feee-11e9-91ff-0025b501a04b', 'marina_levchenko@gmail.com', 'Marina', 'L',
                               'BGKF122kj', '380936912376', 'Olegovna', "", 400, 'lastName must be longer than'
                                                                                 ' or equal to 2 characters')])
    def test_msg_when_last_name_is_too_short(cityUuid, email, firstName, lastName, password, phone,
                                              surname, verifyCode, expected_status_code, expected_message, base_url):
        response = RegistrationPage.get_response(base_url, INNER_URL, cityUuid, email, firstName,
                                                 lastName, password, phone, surname, verifyCode)
        content_msg = RegistrationPage.get_content_message(base_url, INNER_URL, cityUuid, email, firstName, lastName,
                                                           password, phone, surname, verifyCode)
        assert response.status_code == expected_status_code and expected_message in content_msg.values()

    @staticmethod
    @pytest.mark.parametrize("cityUuid, email, firstName, lastName, password, phone, surname, verifyCode, "
                             "expected_status_code, expected_message",
                             [('1b009444-4e4a-11ed-a361-48df37b92096', 'kristina_osadcha@gmail.com',
                               'Kristina', 'Osaaaaaaaaaaadddddddcccchhhhhhaaaaaaa', 'QWD564vf', '380964903845',
                               'Vladimirovna', "", 400, 'lastName must be shorter than or equal to 30 characters'),
                              ('d30282f8-feee-11e9-91ff-0025b501a04b', 'marina_levchenko@gmail.com',
                               'Marina', 'Levvvvvvvvccccccchhhhhheeeeeeennkkkooo', 'BGKF122kj', '380936912376',
                               'Olegovna', "", 400, 'lastName must be shorter than or equal to 30 characters')])
    def test_msg_when_last_name_is_too_long(cityUuid, email, firstName, lastName, password, phone,
                                             surname, verifyCode, expected_status_code, expected_message, base_url):
        response = RegistrationPage.get_response(base_url, INNER_URL, cityUuid, email, firstName,
                                                 lastName, password, phone, surname, verifyCode)
        content_msg = RegistrationPage.get_content_message(base_url, INNER_URL, cityUuid, email, firstName, lastName,
                                                           password, phone, surname, verifyCode)
        assert response.status_code == expected_status_code and expected_message in content_msg.values()

    @staticmethod
    @pytest.mark.parametrize("cityUuid, email, firstName, lastName, password, phone, surname, verifyCode,"
                             " expected_status_code, expected_message",
                             [('1b009444-4e4a-11ed-a361-48df37b92096', 'kristina_osadcha@gmail.com',
                               'Kristina', 'Osadcha', 'QWD564vf', '380964903845', 'V', "",
                               400, 'surname must be longer than or equal to 2 characters'),
                              ('d30282f8-feee-11e9-91ff-0025b501a04b', 'marina_levchenko@gmail.com',
                               'Marina', 'Levchenko', 'BGKF122kj', '380936912376', 'O', "",
                               400, 'surname must be longer than or equal to 2 characters')])
    def test_msg_when_surname_is_too_short(cityUuid, email, firstName, lastName, password, phone,
                                             surname, verifyCode, expected_status_code, expected_message, base_url):
        response = RegistrationPage.get_response(base_url, INNER_URL, cityUuid, email, firstName,
                                                 lastName, password, phone, surname, verifyCode)
        content_msg = RegistrationPage.get_content_message(base_url, INNER_URL, cityUuid, email, firstName, lastName,
                                                           password, phone, surname, verifyCode)
        assert response.status_code == expected_status_code and expected_message in content_msg.values()

    @staticmethod
    @pytest.mark.parametrize("cityUuid, email, firstName, lastName, password, phone, surname, verifyCode, "
                             "expected_status_code, expected_message",
                             [('1b009444-4e4a-11ed-a361-48df37b92096', 'kristina_osadcha@gmail.com',
                               'Kristina', 'Osadcha', 'QWD564vf', '380964903845',
                               'Vladimirrrrooooooovvvvvvnnnnnnaaaaaaaa', "", 400, 'surname must be shorter than or'
                                                                                  ' equal to 30 characters'),
                              ('d30282f8-feee-11e9-91ff-0025b501a04b', 'marina_levchenko@gmail.com',
                               'Marina', 'Levchenko', 'BGKF122kj', '380936912376',
                               'Olllllleeeeeggggggooooooovvvvvvvvnnnna', "", 400, 'surname must be shorter than or '
                                                                                  'equal to 30 characters')])
    def test_msg_when_surname_is_too_long(cityUuid, email, firstName, lastName, password, phone,
                                            surname, verifyCode, expected_status_code, expected_message, base_url):
        response = RegistrationPage.get_response(base_url, INNER_URL, cityUuid, email, firstName,
                                                 lastName, password, phone, surname, verifyCode)
        content_msg = RegistrationPage.get_content_message(base_url, INNER_URL, cityUuid, email, firstName, lastName,
                                                           password, phone, surname, verifyCode)
        assert response.status_code == expected_status_code and expected_message in content_msg.values()

    @staticmethod
    @pytest.mark.parametrize("cityUuid, email, firstName, lastName, password, phone, surname, verifyCode, "
                             "expected_status_code, expected_message",
                             [('1b009444-4e4a-11ed-a361-48df37b92096', 'kristina_osadcha@gmail.com',
                               'Kristina', 'Osadcha', 'QW64v', '380964903845', 'Vladimirivna', "", 400,
                               'password must be longer than or equal to 6 characters'),
                              ('d30282f8-feee-11e9-91ff-0025b501a04b', 'marina_levchenko@gmail.com',
                               'Marina', 'Levchenko', 'BG2kj', '380936912376', 'Olegovna', "", 400,
                               'password must be longer than or equal to 6 characters')])
    def test_msg_when_password_is_too_short(cityUuid, email, firstName, lastName, password, phone,
                                           surname, verifyCode, expected_status_code, expected_message, base_url):
        response = RegistrationPage.get_response(base_url, INNER_URL, cityUuid, email, firstName,
                                                 lastName, password, phone, surname, verifyCode)
        content_msg = RegistrationPage.get_content_message(base_url, INNER_URL, cityUuid, email, firstName, lastName,
                                                           password, phone, surname, verifyCode)
        assert response.status_code == expected_status_code and expected_message in content_msg.values()

    @staticmethod
    @pytest.mark.parametrize("cityUuid, email, firstName, lastName, password, phone, surname, verifyCode, "
                             "expected_status_code, expected_message",
                             [('1b009444-4e4a-11ed-a361-48df37b92096', 'kristina_osadcha@gmail.com',
                               'Kristina', 'Osadcha', 'QWD564vffjfdjsksk333jdvjvjkckxj', '380964903845',
                               'Vladimirovna', "", 400, 'password must be shorter than or equal to 25 characters'),
                              ('d30282f8-feee-11e9-91ff-0025b501a04b', 'marina_levchenko@gmail.com',
                               'Marina', 'Levchenko', 'BGKF122kjgfkdjg4455qcjjkxkxxj34', '380936912376',
                               'Olegovna', "", 400, 'password must be shorter than or equal to 25 characters')])
    def test_msg_when_password_is_too_long(cityUuid, email, firstName, lastName, password, phone,
                                          surname, verifyCode, expected_status_code, expected_message, base_url):
        response = RegistrationPage.get_response(base_url, INNER_URL, cityUuid, email, firstName,
                                                 lastName, password, phone, surname, verifyCode)
        content_msg = RegistrationPage.get_content_message(base_url, INNER_URL, cityUuid, email, firstName, lastName,
                                                           password, phone, surname, verifyCode)
        assert response.status_code == expected_status_code and expected_message in content_msg.values()

    @staticmethod
    @pytest.mark.parametrize("cityUuid, email, firstName, lastName, password, phone, surname, verifyCode, "
                             "expected_status_code, expected_message",
                             [('1b009444-4e4a-11ed-a361-48df37b92096', 'kristina_osadcha@gmail.com',
                               'Kristina', 'Osadcha', 'QW64v45', '380402124087', 'Vladimirivna', "",
                               400, "Phone 380402124087 can't be used or invalid!"),
                              ('d30282f8-feee-11e9-91ff-0025b501a04b', 'marina_levchenko@gmail.com',
                               'Marina', 'Levchenko', 'BG2kjfg', '380481249751', 'Olegovna', "",
                               400, "Phone 380481249751 can't be used or invalid!")])
    def test_msg_incorrect_phone_number(cityUuid, email, firstName, lastName, password, phone,
                                            surname, verifyCode, expected_status_code, expected_message, base_url):
        response = RegistrationPage.get_response(base_url, INNER_URL, cityUuid, email, firstName,
                                                               lastName, password, phone, surname, verifyCode)
        content_msg = RegistrationPage.get_content_message(base_url, INNER_URL, cityUuid, email, firstName, lastName,
                                             password, phone, surname, verifyCode)
        assert response.status_code == expected_status_code and expected_message in content_msg.values()






