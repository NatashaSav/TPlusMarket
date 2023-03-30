import pytest


@pytest.mark.parametrize("test_input, expected_response", [("!@#", 200), ("*&%", 200), ("(&^)", 200), ("+!#", 200),
                                                           ("{@#}", 200), ("$#|&", 200), ("_)&(", 200), ("$%&*", 200)])
def test_special_symbols(before_all_fixture, test_input, expected_response, base_url):
    inner_url = '/api/product/autocomplete'
    my_url = f"{base_url}/{inner_url}"
    params = {'search': test_input}
    response = before_all_fixture.get(url=my_url, params=params)
    assert response.status_code == expected_response
