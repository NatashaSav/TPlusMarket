import pytest
import requests


@pytest.fixture(scope='session', autouse=True)
def before_all_fixture(base_url):
    session = requests.Session()
    inner_url = 'api/auth/refresh'
    my_url = f"{base_url}/{inner_url}"
    response = session.get(my_url)
    data = response.json()
    head = {'Authorization': 'Bearer {}'.format(data['accessToken']),
            'x-request-app': 'Techno+ Marketplace',
            'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1'}
    session.headers.update(head)
    return session













