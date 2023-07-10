import json

import pytest

from pages.login_page import LoginPage

INNER_URL = "api/auth/sign-in"


class TestingLogin:

    @staticmethod
    @pytest.mark.parametrize("email, password, expected_status_code, expected_message",
                             [('kristina_osadcha@gmail.com', 'DFF223fg', 401, 'Email or password is not valid'),
                              ('marina_levchenko@gmail.com', 'BGKF122j', 401, 'Email or password is not valid')])
    @pytest.mark.login
    def test_unregistered_user(email, password, expected_status_code, expected_message, base_url):
        response = LoginPage.get_response_data(base_url, INNER_URL, email, password)
        actual_message = json.loads(response.content)['message']
        assert response.status_code == expected_status_code, f"expect to get status code {expected_status_code}," \
                                                             f" but another status code {response.status_code} appeared"
        assert actual_message == expected_message, f"{actual_message} is not equal {expected_message}"

    @staticmethod
    @pytest.mark.parametrize("email, password, expected_status_code",
                             [('rubanova_olena45@gmail.com', 'Qwert1234', 200)])
    @pytest.mark.login
    def test_successful_login_for_registered_user(email, password, expected_status_code, base_url):
        response = LoginPage.get_response_data(base_url, INNER_URL, email, password)
        assert response.status_code == expected_status_code, f"expect to get status code {expected_status_code}," \
                                                             f" but another status code {response.status_code} appeared"

    @staticmethod
    @pytest.mark.parametrize("email, password, expected_status_code, expected_message",
                             [(' ', 'Qwert1234', 401, "Email or password is not valid"),
                              ('rubanova_olena45@gmail.com', ' ', 401, "Email or password is not valid"),
                              (' ', ' ', 401, "Email or password is not valid")])
    @pytest.mark.login
    def test_login_with_empty_fields(email, password, expected_status_code, expected_message, base_url):
        response = LoginPage.get_response_data(base_url, INNER_URL, email, password)
        actual_message = json.loads(response.content)['message']
        assert response.status_code == expected_status_code, f"expect to get status code {expected_status_code}," \
                                                             f" but another status code {response.status_code} appeared"
        assert actual_message == expected_message, f"{actual_message} is not equal {expected_message}"

    @staticmethod
    @pytest.mark.parametrize("email, password, expected_status_code, expected_message",
                             [('rubanova_olena@gmail.com', 'Qwert1234', 401, "Email or password is not valid"),
                              ('rubanova_olena45@gmail.com', 'Qwer234', 401, "Email or password is not valid")])
    @pytest.mark.login
    def test_login_with_one_correct_and_one_incorrect_fields(email, password, expected_status_code, expected_message,
                                                             base_url):
        response = LoginPage.get_response_data(base_url, INNER_URL, email, password)
        actual_message = json.loads(response.content)['message']
        assert response.status_code == expected_status_code, f"expect to get status code {expected_status_code}," \
                                                             f" but another status code {response.status_code} appeared"
        assert actual_message == expected_message, f"{actual_message} is not equal {expected_message}"

    @staticmethod
    @pytest.mark.parametrize("email, password, expected_status_code, expected_message",
                             [('Qwert1234', 'rubanova_olena45@gmail.com', 401, "Email or password is not valid")])
    @pytest.mark.login
    def test_correct_data_in_incorrect_fields(email, password, expected_status_code, expected_message, base_url):
        response = LoginPage.get_response_data(base_url, INNER_URL, email, password)
        actual_message = json.loads(response.content)['message']
        assert response.status_code == expected_status_code, f"expect to get status code {expected_status_code}," \
                                                             f" but another status code {response.status_code} appeared"
        assert actual_message == expected_message, f"{actual_message} is not equal {expected_message}"

    @staticmethod
    @pytest.mark.parametrize("email, password, expected_status_code, expected_message",
                             [('<script>alert("You have been hacked!")</script>', 'Qwert1234', 401,
                               "Email or password is not valid"),
                              ('rubanova_olena45@gmail.com', '<script>alert("You have been hacked!")</script>', 401,
                               "Email or password is not valid")])
    @pytest.mark.login
    def test_cross_site_scripting_text_in_field(email, password, expected_status_code, expected_message, base_url):
        response = LoginPage.get_response_data(base_url, INNER_URL, email, password)
        actual_message = json.loads(response.content)['message']
        assert response.status_code == expected_status_code, f"expect to get status code {expected_status_code}," \
                                                             f" but another status code {response.status_code} appeared"
        assert actual_message == expected_message, f"{actual_message} is not equal {expected_message}"

    @staticmethod
    @pytest.mark.parametrize("email, password, expected_status_code, expected_message",
                             [("SELECT * FROM users WHERE username = '' OR 1=1-- ' AND password = 'foo'", 'Qwert1234',
                               401, "Email or password is not valid"),
                              ('rubanova_olena45@gmail.com', "SELECT * FROM products WHERE id = 10; DROP members--",
                               401, "Email or password is not valid")])
    @pytest.mark.login
    def test_sql_injections(email, password, expected_status_code, expected_message, base_url):
        response = LoginPage.get_response_data(base_url, INNER_URL, email, password)
        actual_message = json.loads(response.content)['message']
        assert response.status_code == expected_status_code, f"expect to get status code {expected_status_code}," \
                                                             f" but another status code {response.status_code} appeared"
        assert actual_message == expected_message, f"{actual_message} is not equal {expected_message}"

    @staticmethod
    @pytest.mark.parametrize("email, password, expected_status_code, expected_message",
                             [("(<form action=”http://live.hh.ru”><input type=”submit”></form>)", 'Qwert1234',
                               401, "Email or password is not valid"),
                              ('rubanova_olena45@gmail.com',
                               "(<form action=”https://rahulshettyacademy.com/”><input type=”submit”></form>)",
                               401, "Email or password is not valid")])
    @pytest.mark.login
    def test_html_tags_in_login_fields(email, password, expected_status_code, expected_message, base_url):
        response = LoginPage.get_response_data(base_url, INNER_URL, email, password)
        actual_message = json.loads(response.content)['message']
        assert response.status_code == expected_status_code, f"expect to get status code {expected_status_code}," \
                                                             f" but another status code {response.status_code} appeared"
        assert actual_message == expected_message, f"{actual_message} is not equal {expected_message}"

    @staticmethod
    @pytest.mark.parametrize("email, password, expected_status_code, expected_message",
                             [("♣☺♂”,“”‘~!@#$%^&*()?>,./\<][ /*<!–“”, “${code}”;–>", 'Qwert1234', 401,
                               "Email or password is not valid"),
                              ('rubanova_olena45@gmail.com', "(@”?>±,“”‘@#$%^&*>,./\<][?!@#$%6+–”,“${!add}!±”;>–", 401,
                               "Email or password is not valid")])
    @pytest.mark.login
    def test_complex_sequence_of_symbols_in_fields(email, password, expected_status_code, expected_message, base_url):
        response = LoginPage.get_response_data(base_url, INNER_URL, email, password)
        actual_message = json.loads(response.content)['message']
        assert response.status_code == expected_status_code, f"expect to get status code {expected_status_code}," \
                                                             f" but another status code {response.status_code} appeared"
        assert actual_message == expected_message, f"{actual_message} is not equal {expected_message}"

    @staticmethod
    @pytest.mark.parametrize("email, password, expected_status_code, expected_message",
                             [('  rubanova_olena@gmail.com', 'Qwert1234', 401, "Email or password is not valid"),
                              ('rubanova_olena@gmail.com  ', 'Qwert1234', 401, "Email or password is not valid"),
                              ('rubanova_olena45@gmail.com', '  Qwert234', 401, "Email or password is not valid"),
                              ('rubanova_olena45@gmail.com', 'Qwert234  ', 401, "Email or password is not valid")])
    @pytest.mark.login
    def test_login_with_correct_data_and_spaces(email, password, expected_status_code, expected_message, base_url):
        response = LoginPage.get_response_data(base_url, INNER_URL, email, password)
        actual_message = json.loads(response.content)['message']
        assert response.status_code == expected_status_code, f"expect to get status code {expected_status_code}," \
                                                             f" but another status code {response.status_code} appeared"
        assert actual_message == expected_message, f"{actual_message} is not equal {expected_message}"

    @staticmethod
    @pytest.mark.parametrize("email, password, expected_status_code, expected_message",
                             [('RUBanovA_olENa@gmaIL.cOm', 'Qwert1234', 401, "Email or password is not valid"),
                              ('rubaNOVa_OLEna@gmail.CoM', 'Qwert1234', 401, "Email or password is not valid"),
                              ('rubanova_olena45@gmail.com', 'qWERT234', 401, "Email or password is not valid"),
                              ('rubanova_olena45@gmail.com', 'qWeRt234', 401, "Email or password is not valid")])
    @pytest.mark.login
    def test_login_with_correct_data_using_mixed_case_letters(email, password, expected_status_code, expected_message,
                                                              base_url):
        response = LoginPage.get_response_data(base_url, INNER_URL, email, password)
        actual_message = json.loads(response.content)['message']
        assert response.status_code == expected_status_code, f"expect to get status code {expected_status_code}," \
                                                             f" but another status code {response.status_code} appeared"
        assert actual_message == expected_message, f"{actual_message} is not equal {expected_message}"

    @staticmethod
    @pytest.mark.parametrize("email, password, expected_status_code, expected_message",
                             [('rdkkvvjdovdvvlvlvnoreernbgvbbffbkdsfgdhfjmnbvcxbbmdkdckvmvvfjfjfjldqzxmcnckdjdowflbdsgg'
                               'ggghhhhhbbnnmmllyuojnazxcvbnkhgf', 'Qwert1234', 401, "Email or password is not valid"),
                              ('rubanova_olena45@gmail.com', 'sdfghnkbfdsawertyuikmnbvcxsdfrghjmknbvcxzsdefrgthjnb'
                               'vcxszdfghnjbvcxsdfghnjmnbvcxzsdfghbn', 401, "Email or password is not valid")])
    @pytest.mark.login
    def test_login_with_too_long_data(email, password, expected_status_code, expected_message, base_url):
        response = LoginPage.get_response_data(base_url, INNER_URL, email, password)
        actual_message = json.loads(response.content)['message']
        assert response.status_code == expected_status_code, f"expect to get status code {expected_status_code}," \
                                                             f" but another status code {response.status_code} appeared"
        assert actual_message == expected_message, f"{actual_message} is not equal {expected_message}"
