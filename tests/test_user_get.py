import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure

@allure.epic("Get user details cases")
class TestUserGet(BaseCase):
    data = {
        'email': 'vinkotov@example.com',
        'password': '1234'
    }

    @allure.description("This test gets details of non-authorized user")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.testcase('https://exsample_tms.com/api/test-get-user-det-not-auth', name='Testcase 21')
    @allure.feature('Negative')
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    @allure.description("This test gets details of an authorized user")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.testcase('https://exsample_tms.com/api/test-get-user-det-auth-as-same', name='Testcase 22')
    @allure.feature('Positive')
    def test_get_user_details_auth_as_same_user(self):

        response1 = MyRequests.post("/user/login", data=self.data)
        auth_sid = self.get_cookie(response1,"auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_from_auth_method = self.get_json_value(response1, "user_id")
        response2 = MyRequests.get(
            f"/user/{user_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    @allure.description("This test gets user details, when another user was authorized")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase('https://exsample_tms.com/api/test-get-user-det-auth-as-another', name='Testcase 23')
    @allure.feature('Negative')
    def test_get_user_details_auth_as_another_user(self):
        response1 = MyRequests.post("/user/login", data=self.data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_from_auth_method = self.get_json_value(response1, "user_id")
        response2 = MyRequests.get(
            f"/user/{user_from_auth_method+200}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_json_has_key(response2, "username")
        Assertions.assert_json_has_not_key(response2, "email")
        Assertions.assert_json_has_not_key(response2, "firstName")
        Assertions.assert_json_has_not_key(response2, "lastName")