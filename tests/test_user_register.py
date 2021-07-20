import requests
import pytest
import random
import string
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure

@allure.epic("Registration cases")
class TestUserRegister(BaseCase):

    @allure.description("This test successfully creates user")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.testcase('https://exsample_tms.com/api/test-user-reg', name='Testcase 11')
    @allure.feature('Positive')
    def test_create_user_successfully(self):
        with allure.step("Preparing registration data"):
            data = self.prepare_registration_data()
        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response,"id")

    @allure.description("This test checks registration with existing email")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.testcase('https://exsample_tms.com/api/test-user-exist-email', name='Testcase 12')
    @allure.feature('Negative')
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        with allure.step("Preparing registration data"):
            data = self.prepare_registration_data(email)
        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_content(response, f"Users with email '{email}' already exists")

    @allure.description("This test checks registration with wrong email")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.testcase('https://exsample_tms.com/api/test-user-wrong-email', name='Testcase 13')
    @allure.feature('Negative')
    def test_create_user_with_wrong_email(self):
        email = 'vinkotov.example.com'
        with allure.step("Preparing registration data"):
            data = self.prepare_registration_data(email)
        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 400)
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

    @allure.description("This test checks registration w/o one of fields")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase('https://exsample_tms.com/api/test-neg-auth', name='Testcase 14')
    @allure.issue('http://www.mytesttracker.com/issue/2136')
    @allure.feature('Negative')
    @pytest.mark.parametrize('data', regData)
    def test_create_user_without_one_of_fields(self, data):
        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 400)
        dif_fields = set(self.prepare_registration_data().keys())-set(dict(data).keys())
        for field in dif_fields:
            Assertions.assert_content(response, f"The following required params are missed: {field}")

    @allure.description("This test checks registration with short name")
    @allure.severity(allure.severity_level.MINOR)
    @allure.testcase('https://exsample_tms.com/api/test-user-short-name', name='Testcase 15')
    @allure.feature('Negative')
    def test_create_user_with_short_name(self):
        with allure.step("Preparing registration data"):
            data = self.prepare_registration_data(username="a")
        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_content(response, "The value of 'username' field is too short")

    @allure.description("This test checks registration with long name")
    @allure.severity(allure.severity_level.MINOR)
    @allure.testcase('https://exsample_tms.com/api/test-user-short-name', name='Testcase 16')
    @allure.feature('Negative')
    def test_create_user_with_long_name(self):
        username = ''.join(random.choice(string.ascii_lowercase) for i in range(256))
        with allure.step("Preparing registration data"):
            data = self.prepare_registration_data()
            data['username'] = username
        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_content(response, "The value of 'username' field is too long")
