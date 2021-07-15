import requests
import pytest
import random
import string
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

class TestUserRegister(BaseCase):

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        response = MyRequests.post("/user", data=data)
        # assert response.status_code == 200, f"Unexpected status code {response.status_code}"
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response,"id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user", data=data)
        #assert response.status_code == 400, f"Unexpected status code {response.status_code}"
        Assertions.assert_code_status(response, 400)
        # assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"
        Assertions.assert_content(response, f"Users with email '{email}' already exists")

    def test_create_user_with_wrong_email(self):
        email = 'vinkotov.example.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user", data=data)
        # print(response.status_code)
        Assertions.assert_code_status(response, 400)
        # print(response.content)
        Assertions.assert_content(response, "Invalid email format")

    regData = [
        {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
        },
        {
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'ir_z@example.com'
        },
        {
            'password': '123',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'ir_z1@example.com'
        },
        {
            'password': '123',
            'username': 'learnqa',
            'lastName': 'learnqa',
            'email': 'ir_z2@example.com'
        },
        {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'email': 'ir_z3@example.com'
        }

    ]

    @pytest.mark.parametrize('data', regData)
    def test_create_user_without_one_of_fields(self, data):
        response = MyRequests.post("/user", data=data)
        #print(response.status_code)
        Assertions.assert_code_status(response, 400)
        #print(response.content)
        dif_fields = set(self.prepare_registration_data().keys())-set(dict(data).keys())
        #print(dif_fields)
        for field in dif_fields:
            Assertions.assert_content(response, f"The following required params are missed: {field}")

    def test_create_user_with_short_name(self):
        data = self.prepare_registration_data(username="a")
        response = MyRequests.post("/user", data=data)
        #print(response.status_code)
        Assertions.assert_code_status(response, 400)
        #print(response.content)
        Assertions.assert_content(response, "The value of 'username' field is too short")

    def test_create_user_with_long_name(self):
        username = ''.join(random.choice(string.ascii_lowercase) for i in range(256))
        data = self.prepare_registration_data()
        data['username']=username
        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 400)
        #print(response.status_code)
        Assertions.assert_content(response, "The value of 'username' field is too long")
        #print(response.content)
