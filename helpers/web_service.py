import requests
import re


class WebService:
    def __init__(self, base_url: str):
        self.session = requests.session()
        self.base_url = base_url

    def _get_token(self, url: str):
        rsp = self.session.get(self.base_url + url)
        mutch = re.search('<input type="hidden" name="csrfmiddlewaretoken" value="(.+?)">', rsp.text)
        if mutch:
            return mutch.group(1)
        else:
            assert False, 'Failed to get token'

    def login_post(self, username: str, password: str):
        token = self._get_token('/login/')
        data = {
            'username': username,
            'password': password,
            'csrfmiddlewaretoken': token
        }
        self.session.post(self.base_url + '/login/', data=data)
        csrftoken = self.session.cookies.get('csrftoken')
        self.session.headers.update({'X-CSRFToken': csrftoken})

    def create_testcase_post(self, testname: str, testdescription: str):
        token = self._get_token('/test/new')
        data = {
            'testname': testname,
            'testdescription': testdescription,
            'csrfmiddlewaretoken': token
        }
        response = self.session.post(self.base_url + '/test/new', data=data)
        if response.status_code != 200:
            raise AssertionError(f"An invalid status code was received: {response.status_code}")


    def close(self):
        self.session.close()
