import pytest
import requests
import json

from pages.base_page import BasePage
from pages.registration_page import RegistrationPage

INNER_URL = "api/auth/sign-up"


class TestingRegistration:

    @staticmethod
    @pytest.mark.parametrize("cityUuid, email, firstName, lastName, password, phone, surname, verification_code, "
                             "expected_status_code",
                             [('1b009444-4e4a-11ed-a361-48df37b92096', 'lana_vincko@gmail.com',
                               'Lana', 'Vincnko', 'FKGVB334fs', '380960393670', 'Vladimirovna', '1111', 200)])
    @pytest.mark.skip(reason="user can be registered once")
    def test_succesful_user_registration(cityUuid, email, firstName, lastName, password, phone,
                                              surname, verification_code, expected_status_code, base_url):
        response = RegistrationPage.get_response(base_url, INNER_URL, cityUuid, email, firstName, lastName, password,
                                                 phone, surname)
        content_msg = RegistrationPage.get_extended_response(base_url, INNER_URL, response, verification_code)
        assert content_msg.status_code == expected_status_code, f"expect to get status code {expected_status_code}," \
                                                             f" but another status code {response.status_code} appeared"

    @staticmethod
    @pytest.mark.parametrize("cityUuid, email, firstName, lastName, password, phone, surname, verification_code,"
                             "expected_status_code, expected_message",
                             [('1b009444-4e4a-11ed-a361-48df37b92096', 'marina_evchenko@gmail.com',
                               'Marina', 'Evchenko', 'FKGJD334fs', '380960361670', 'Vladimirovna', '1111', 400,
                               'User with these mail or phone already exists')])
    def test_user_registration_with_same_phone_number(cityUuid, email, firstName, lastName, password, phone,
                                         surname, verification_code, expected_status_code, expected_message, base_url):
        response = RegistrationPage.get_response(base_url, INNER_URL, cityUuid, email, firstName, lastName, password,
                                                 phone, surname)
        content_msg = RegistrationPage.get_content_message_with_extended_payload(base_url, INNER_URL, response,
                                                                                 verification_code)
        assert response.status_code == expected_status_code, f"expect to get status code {expected_status_code}," \
                                                             f" but another status code {response.status_code} appeared"
        assert expected_message == content_msg


    @staticmethod
    @pytest.mark.parametrize("cityUuid, email, firstName, lastName, password, phone, surname, verification_code, "
                             "expected_status_code, expected_message",
                             [('1b009444-4e4a-11ed-a361-48df37b92096', 'marina_evchenko@gmail.com',
                               'Ilona', 'Lavoda', 'FKGJD334fs', '380960361670', 'Dimirovna', '1111', 400,
                               'User with these mail or phone already exists')])
    def test_user_registration_with_same_email(cityUuid, email, firstName, lastName, password, phone, surname,
                                               verification_code, expected_status_code, expected_message, base_url):
        response = RegistrationPage.get_response(base_url, INNER_URL, cityUuid, email, firstName, lastName, password,
                                                 phone, surname)
        content_msg = RegistrationPage.get_content_message_with_extended_payload(base_url, INNER_URL, response,
                                                                                 verification_code)
        assert response.status_code == expected_status_code, f"expect to get status code {expected_status_code}," \
                                                             f" but another status code {response.status_code} appeared"
        assert expected_message == content_msg

    @staticmethod
    @pytest.mark.parametrize("cityUuid, email, firstName, lastName, password, phone, surname, expected_status_code",
                             [('d30282f8-feee-11e9-91ff-0025b501a04b', 'olga_yanko@gmail.com',
                               'Olga', 'Yanko', 'BGKF122kj', '380936956567', 'Olegovna', 200)])
    def test_successful_user_status_code(cityUuid, email, firstName, lastName, password, phone,
                                         surname, expected_status_code, base_url):
        response = RegistrationPage.get_response(base_url, INNER_URL, cityUuid, email, firstName, lastName, password,
                                                 phone, surname)
        assert response.status_code == expected_status_code, f"expect to get status code {expected_status_code}," \
                                                             f" but another status code {response.status_code} appeared"

    @staticmethod
    @pytest.mark.parametrize("cityUuid, email, firstName, lastName, password, phone, surname, verification_code, "
                             "expected_status_code, expected_message",
                             [('', 'kristina_osadcha@gmail.com', 'Kristina', 'Osadcha', 'QWD564vf', '380964903845',
                               'Vladimirovna', '1111', 400, 'cityUuid should not be empty'),
                              ('1b009444-4e4a-11ed-a361-48df37b92096', '', 'Kristina', 'Osadcha', 'QWD564vf',
                               '380964903845', 'Vladimirovna', '1111', 400, 'email must be longer than or equal to'
                                                                       ' 6 characters'),
                              ('1b009444-4e4a-11ed-a361-48df37b92096', 'kristina_osadcha@gmail.com', '', 'Osadcha',
                               'QWD564v', '380964903845', 'Vladimirovna', '1111', 400, 'firstName should not be empty'),
                              ('1b009444-4e4a-11ed-a361-48df37b92096', 'kristina_osadcha@gmail.com', 'Kristina',
                               '', 'QWD564vf', '380964903845', 'Vladimirovna', '1111', 400, 'lastName should not be'
                                                                                            ' empty'),
                              ('1b009444-4e4a-11ed-a361-48df37b92096', 'kristina_osadcha@gmail.com', 'Kristina',
                               'Osadcha', '', '380964903845', 'Vladimirovna', '1111', 400, 'password should not be '
                                                                                           'empty'),
                              ('1b009444-4e4a-11ed-a361-48df37b92096', 'kristina_osadcha@gmail.com', 'Kristina',
                               'Osadcha', 'QWD564vf', '', 'Vladimirovna', '1111', 400, 'phone should not be empty'),
                              ('1b009444-4e4a-11ed-a361-48df37b92096', 'kristina_osadcha@gmail.com', 'Kristina',
                               'Osadcha', 'QWD564vf', '380964903845', '', '1111', 400, 'surname should not be empty'),
                              ('1b009444-4e4a-11ed-a361-48df37b92096', 'kristina_osadcha@gmail.com', 'Kristina',
                               'Osadcha', 'QWD564vf', '380964903845', 'Vladimirovna', '', 400, 'verifyCode must be a '
                                                                                               'number string')
                              ])
    def test_registration_user_with_empty_field(before_all_fixture, cityUuid, email, firstName, lastName, password,
                                                phone, surname, verification_code, expected_status_code,
                                                expected_message, base_url):
        response = RegistrationPage.get_response(base_url, INNER_URL, cityUuid, email, firstName, lastName, password,
                                                 phone, surname)
        content_msg = RegistrationPage.get_content_message_with_extended_payload(base_url, INNER_URL, response,
                                                                                 verification_code)
        assert response.status_code == expected_status_code, f"expect to get status code {expected_status_code}," \
                                                             f" but another status code {response.status_code} appeared"
        assert expected_message in content_msg.values()

    @staticmethod
    @pytest.mark.parametrize("cityUuid, email, firstName, lastName, password, phone, surname, verification_code, "
                             "expected_message",
                             [('1b009444-4e4a-11ed-a361-48df37b92096', 'irina_osadcha@gmail.com', 'Irina', 'Osadcha',
                               'ssk233jd', '380964967800', 'Vladimirovna', '234', 'verifyCode must be longer than'
                                                                                       ' or equal to 4 characters'),
                              ('1b009444-4e4a-11ed-a361-48df37b92096', 'irina_osadcha@gmail.com', 'Irina', 'Osadcha',
                               'ssk233jd', '380964903000', 'Vladimirovna', '123456', 'verifyCode must be shorter than '
                                                                                     'or equal to 4 characters')
                              ])
    def test_len_verification_code_msg(before_all_fixture, cityUuid, email, firstName, lastName, password, phone,
                                       surname, verification_code, expected_message, base_url):
        response = RegistrationPage.get_response(base_url, INNER_URL, cityUuid, email, firstName, lastName, password,
                                                 phone, surname)
        content_msg = RegistrationPage.get_content_message_with_extended_payload(base_url, INNER_URL, response,
                                                                                 verification_code)
        assert expected_message in content_msg.values()


    @staticmethod
    @pytest.mark.parametrize("cityUuid, email, firstName, lastName, password, phone, surname, verification_code, "
                             "expected_message",
                             [('1b009444-4e4a-11ed-a361-48df37b92096', 'olena_vlasova@gmail.com',
                               'Olena', 'Vlasova', 'QWD564vf', '380964903909', 'Vladimirovna', '1276', 'Invalid '
                                                                                                'verification code')])
    def test_invalid_verification_code(before_all_fixture, cityUuid, email, firstName, lastName, password, phone,
                                         surname, verification_code, expected_message, base_url):
        response = RegistrationPage.get_response(base_url, INNER_URL, cityUuid, email, firstName, lastName, password,
                                                 phone, surname)
        content_msg = RegistrationPage.get_content_message_with_extended_payload(base_url, INNER_URL, response,
                                                                                 verification_code)
        assert expected_message in content_msg.values()

    @staticmethod
    @pytest.mark.parametrize("cityUuid, email, firstName, lastName, password, phone, surname, expected_status_code, "
                             "verification_code, expected_message",
                             [('1b009444-4e4a-11ed-a361-48df37b92096', 'kristina_osadcha#g.com',
                               'Kristina', 'Osadcha', 'QWD564vf', '380964903845', 'Vladimirovna', 400, '1111',
                               'email must be an email'),
                              ('d30282f8-feee-11e9-91ff-0025b501a04b', 'kristi$gmail.com',
                               'Marina', 'Levchenko', 'BGKF122kj', '380936912376', 'Olegovna', 400, '1111',
                               'email must be an email')])
    def test_incorrect_email(cityUuid, email, firstName, lastName, password, phone, surname, expected_status_code,
                             verification_code, expected_message, base_url):
        response = RegistrationPage.get_response(base_url, INNER_URL, cityUuid, email, firstName, lastName, password,
                                                 phone, surname)
        content_msg = RegistrationPage.get_content_message_with_extended_payload(base_url, INNER_URL, response,
                                                                                 verification_code)
        assert response.status_code == expected_status_code, f"expect to get status code {expected_status_code}," \
                                                             f" but another status code {response.status_code} appeared"
        assert expected_message in content_msg.values()

    @staticmethod
    @pytest.mark.parametrize("cityUuid, email, firstName, lastName, password, phone, surname, expected_status_code, "
                             "verification_code, expected_message",
                             [('1b009444-4e4a-11ed-a361-48df37b92096', 'kristina_osadcha@gmail.com',
                               'K', 'Osadcha', 'QWD564vf', '380964903845', 'Vladimirovna', 400, '1111',
                               'firstName must be longer than or equal to 2 characters'),
                              ('d30282f8-feee-11e9-91ff-0025b501a04b', 'marina_levchenko@gmail.com',
                               'M', 'Levchenko', 'BGKF122kj', '380936912376', 'Olegovna', 400, '1111',
                               'firstName must be longer than or equal to 2 characters')])
    def test_msg_when_first_name_is_too_short(cityUuid, email, firstName, lastName, password, phone,
                                         surname, expected_status_code, verification_code, expected_message, base_url):
        response = RegistrationPage.get_response(base_url, INNER_URL, cityUuid, email, firstName, lastName, password,
                                                 phone, surname)
        content_msg = RegistrationPage.get_content_message_with_extended_payload(base_url, INNER_URL, response,
                                                                                 verification_code)
        assert response.status_code == expected_status_code, f"expect to get status code {expected_status_code}," \
                                                             f" but another status code {response.status_code} appeared"
        assert expected_message in content_msg.values()



    @staticmethod
    @pytest.mark.parametrize("cityUuid, email, firstName, lastName, password, phone, surname, expected_status_code,"
                             " verification_code, expected_message",
                             [('1b009444-4e4a-11ed-a361-48df37b92096', 'kristina_osadcha@gmail.com',
                               'Kristiiiiiiiiiiiiiiiiiiiiinnnnnnnnnnaaa', 'Osadcha', 'QWD564vf', '380964903845',
                               'Vladimirovna', 400, '1111', 'firstName must be shorter than or equal to 30 characters'),
                              ('d30282f8-feee-11e9-91ff-0025b501a04b', 'marina_levchenko@gmail.com',
                               'Maaaaaaarrriiinnnnnnnnnnnnnnnnaaaaaaaaa', 'Levchenko', 'BGKF122kj', '380936912376',
                               'Olegovna', 400, '1111', 'firstName must be shorter than or equal to 30 characters')])
    def test_msg_when_first_name_is_too_long(cityUuid, email, firstName, lastName, password, phone, surname,
                                             expected_status_code, verification_code, expected_message, base_url):
        response = RegistrationPage.get_response(base_url, INNER_URL, cityUuid, email, firstName, lastName, password,
                                                 phone, surname)
        content_msg = RegistrationPage.get_content_message_with_extended_payload(base_url, INNER_URL, response,
                                                                                 verification_code)
        assert response.status_code == expected_status_code, f"expect to get status code {expected_status_code}," \
                                                             f" but another status code {response.status_code} appeared"
        assert expected_message in content_msg.values()

    @staticmethod
    @pytest.mark.xfail(reason="expect to get status code 400, but another status code appeared")
    @pytest.mark.parametrize("cityUuid, email, firstName, lastName, password, phone, surname, expected_status_code, "
                             "verification_code, expected_message",
                             [('1b009444-4e4a-11ed-a361-48df37b92096', 'kristina_osadcha@gmail.com',
                               'Kristina', 'O', 'QWD564vf', '380964903845', 'Vladimirovna', 400, '1111', 'lastName '
                                                                        'must be longer than or equal to 2 characters'),
                              ('d30282f8-feee-11e9-91ff-0025b501a04b', 'marina_levchenko@gmail.com', 'Marina', 'L',
                               'BGKF122kj', '380936912376', 'Olegovna', 400, '1111', 'lastName must be longer than'
                                                                                 ' or equal to 2 characters')])
    def test_msg_when_last_name_is_too_short(cityUuid, email, firstName, lastName, password, phone, surname,
                                             expected_status_code, verification_code, expected_message, base_url):
        response = RegistrationPage.get_response(base_url, INNER_URL, cityUuid, email, firstName, lastName, password,
                                                 phone, surname)
        content_msg = RegistrationPage.get_content_message_with_extended_payload(base_url, INNER_URL, response,
                                                                                 verification_code)
        assert response.status_code == expected_status_code, f"expect to get status code {expected_status_code}," \
                                                             f" but another status code {response.status_code} appeared"
        assert expected_message in content_msg.values()

    @staticmethod
    @pytest.mark.parametrize("cityUuid, email, firstName, lastName, password, phone, surname, expected_status_code, "
                             "verification_code, expected_message",
                             [('1b009444-4e4a-11ed-a361-48df37b92096', 'kristina_osadcha@gmail.com',
                               'Kristina', 'Osaaaaaaaaaaadddddddcccchhhhhhaaaaaaa', 'QWD564vf', '380964903845',
                               'Vladimirovna', 400, '1111', 'lastName must be shorter than or equal to 30 characters'),
                              ('d30282f8-feee-11e9-91ff-0025b501a04b', 'marina_levchenko@gmail.com',
                               'Marina', 'Levvvvvvvvccccccchhhhhheeeeeeennkkkooo', 'BGKF122kj', '380936912376',
                               'Olegovna', 400, '1111', 'lastName must be shorter than or equal to 30 characters')])
    def test_msg_when_last_name_is_too_long(cityUuid, email, firstName, lastName, password, phone, surname,
                                            expected_status_code, verification_code, expected_message, base_url):
        response = RegistrationPage.get_response(base_url, INNER_URL, cityUuid, email, firstName, lastName, password,
                                                 phone, surname)
        content_msg = RegistrationPage.get_content_message_with_extended_payload(base_url, INNER_URL, response,
                                                                                 verification_code)
        assert response.status_code == expected_status_code, f"expect to get status code {expected_status_code}," \
                                                             f" but another status code {response.status_code} appeared"
        assert expected_message in content_msg.values()

    @staticmethod
    @pytest.mark.parametrize("cityUuid, email, firstName, lastName, password, phone, surname, expected_status_code, "
                             "verification_code, expected_message",
                             [('1b009444-4e4a-11ed-a361-48df37b92096', 'kristina_osadcha@gmail.com',
                               'Kristina', 'Osadcha', 'QWD564vf', '380964903845', 'V', 400, '1111',
                               'surname must be longer than or equal to 2 characters'),
                              ('d30282f8-feee-11e9-91ff-0025b501a04b', 'marina_levchenko@gmail.com',
                               'Marina', 'Levchenko', 'BGKF122kj', '380936912376', 'O', 400, '1111',
                               'surname must be longer than or equal to 2 characters')])
    def test_msg_when_surname_is_too_short(cityUuid, email, firstName, lastName, password, phone, surname,
                                           expected_status_code, verification_code, expected_message, base_url):
        response = RegistrationPage.get_response(base_url, INNER_URL, cityUuid, email, firstName, lastName, password,
                                                 phone, surname)
        content_msg = RegistrationPage.get_content_message_with_extended_payload(base_url, INNER_URL, response,
                                                                                 verification_code)
        assert response.status_code == expected_status_code, f"expect to get status code {expected_status_code}," \
                                                             f" but another status code {response.status_code} appeared"
        assert expected_message in content_msg.values()

    @staticmethod
    @pytest.mark.parametrize("cityUuid, email, firstName, lastName, password, phone, surname, expected_status_code, "
                             "verification_code, expected_message",
                             [('1b009444-4e4a-11ed-a361-48df37b92096', 'kristina_osadcha@gmail.com',
                               'Kristina', 'Osadcha', 'QWD564vf', '380964903845',
                               'Vladimirrrrooooooovvvvvvnnnnnnaaaaaaaa', 400, '1111', 'surname must be shorter than or'
                                                                                  ' equal to 30 characters'),
                              ('d30282f8-feee-11e9-91ff-0025b501a04b', 'marina_levchenko@gmail.com',
                               'Marina', 'Levchenko', 'BGKF122kj', '380936912376',
                               'Olllllleeeeeggggggooooooovvvvvvvvnnnna', 400, '1111', 'surname must be shorter than or '
                                                                                  'equal to 30 characters')])
    def test_msg_when_surname_is_too_long(cityUuid, email, firstName, lastName, password, phone, surname,
                                          expected_status_code, verification_code, expected_message, base_url):
        response = RegistrationPage.get_response(base_url, INNER_URL, cityUuid, email, firstName, lastName, password,
                                                 phone, surname)
        content_msg = RegistrationPage.get_content_message_with_extended_payload(base_url, INNER_URL, response,
                                                                                 verification_code)
        assert response.status_code == expected_status_code, f"expect to get status code {expected_status_code}," \
                                                             f" but another status code {response.status_code} appeared"
        assert expected_message in content_msg.values()

    @staticmethod
    @pytest.mark.parametrize("cityUuid, email, firstName, lastName, password, phone, surname, expected_status_code, "
                             "verification_code, expected_message",
                             [('1b009444-4e4a-11ed-a361-48df37b92096', 'kristina_osadcha@gmail.com',
                               'Kristina', 'Osadcha', 'QW64v', '380964903845', 'Vladimirivna', 400, '1111', 'password '
                                                                       'must be longer than or equal to 6 characters'),
                              ('d30282f8-feee-11e9-91ff-0025b501a04b', 'marina_levchenko@gmail.com',
                               'Marina', 'Levchenko', 'BG2kj', '380936912376', 'Olegovna', 400, '1111', 'password must '
                                                                           'be longer than or equal to 6 characters')])
    def test_msg_when_password_is_too_short(cityUuid, email, firstName, lastName, password, phone, surname,
                                            expected_status_code, verification_code, expected_message, base_url):
        response = RegistrationPage.get_response(base_url, INNER_URL, cityUuid, email, firstName, lastName, password,
                                                 phone, surname)
        content_msg = RegistrationPage.get_content_message_with_extended_payload(base_url, INNER_URL, response,
                                                                                 verification_code)
        assert response.status_code == expected_status_code, f"expect to get status code {expected_status_code}," \
                                                             f" but another status code {response.status_code} appeared"
        assert expected_message in content_msg.values()


    @staticmethod
    @pytest.mark.parametrize("cityUuid, email, firstName, lastName, password, phone, surname, expected_status_code, "
                             "verification_code, expected_message",
                             [('1b009444-4e4a-11ed-a361-48df37b92096', 'kristina_osadcha@gmail.com',
                               'Kristina', 'Osadcha', 'QWD564vffjfdjsksk333jdvjvjkckxj', '380964903845',
                               'Vladimirovna', 400, '1111', 'password must be shorter than or equal to 25 characters'),
                              ('d30282f8-feee-11e9-91ff-0025b501a04b', 'marina_levchenko@gmail.com',
                               'Marina', 'Levchenko', 'BGKF122kjgfkdjg4455qcjjkxkxxj34', '380936912376',
                               'Olegovna', 400, '1111', 'password must be shorter than or equal to 25 characters')])
    def test_msg_when_password_is_too_long(cityUuid, email, firstName, lastName, password, phone, surname,
                                           expected_status_code, verification_code, expected_message, base_url):
        response = RegistrationPage.get_response(base_url, INNER_URL, cityUuid, email, firstName, lastName, password,
                                                 phone, surname)
        content_msg = RegistrationPage.get_content_message_with_extended_payload(base_url, INNER_URL, response,
                                                                                 verification_code)
        assert response.status_code == expected_status_code, f"expect to get status code {expected_status_code}," \
                                                             f" but another status code {response.status_code} appeared"
        assert expected_message in content_msg.values()

    @staticmethod
    @pytest.mark.parametrize("cityUuid, email, firstName, lastName, password, phone, surname, expected_status_code, "
                             "verification_code, expected_message",
                             [('1b009444-4e4a-11ed-a361-48df37b92096', 'kristina_osadcha@gmail.com',
                               'Kristina', 'Osadcha', 'QW64v45', '380402124087', 'Vladimirivna', 400, '1111',
                               "Phone 380402124087 can't be used or invalid!"),
                              ('d30282f8-feee-11e9-91ff-0025b501a04b', 'marina_levchenko@gmail.com',
                               'Marina', 'Levchenko', 'BG2kjfg', '380481249751', 'Olegovna', 400, '1111',
                               "Phone 380481249751 can't be used or invalid!")])
    def test_msg_incorrect_phone_number(cityUuid, email, firstName, lastName, password, phone, surname,
                                        expected_status_code, verification_code, expected_message, base_url):
        response = RegistrationPage.get_response(base_url, INNER_URL, cityUuid, email, firstName, lastName, password,
                                                 phone, surname)
        content_msg = RegistrationPage.get_content_message_with_extended_payload(base_url, INNER_URL, response,
                                                                                 verification_code)
        assert response.status_code == expected_status_code, f"expect to get status code {expected_status_code}," \
                                                             f" but another status code {response.status_code} appeared"
        assert expected_message in content_msg.values()
