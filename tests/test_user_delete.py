import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

class TestUserDelete(BaseCase):

    def test_delete_user_2(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        # LOGIN user 2
        response1 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id = self.get_json_value(response1, "user_id")

        # DELETE use 2
        response2 = MyRequests.delete(f"/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 )

        Assertions.assert_code_status(response2, 400)
        #print(response2.status_code)
        Assertions.assert_content(response2, "Please, do not delete test users with ID 1, 2, 3, 4 or 5.")
        #print(response2.content)

        # GET user 2

        response3 = MyRequests.get(f"/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 )

        Assertions.assert_code_status(response3, 200)
        Assertions.assert_json_value_by_name(
            response3,
            "id",
            str(user_id),
            f"User with id {user_id} doesn't exist (was deleted)"
        )
        Assertions.assert_json_value_by_name(
            response3,
            "email",
            data['email'],
            f"User with email {user_id} doesn't exist (was deleted)"
        )

    def test_delete_new_user(self):
        # REGISTER user
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")
        login_data = {
            'email': email,
            'password': password
        }

        # LOGIN user
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # DELETE user
        response3 = MyRequests.delete(f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_code_status(response3, 200)

        # GET user
        response4 = MyRequests.get(f"/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 )

        #print(response4.status_code)
        Assertions.assert_code_status(response4, 404)
        #print(response4.content)
        Assertions.assert_content(response4, "User not found")

    def test_delete_auth_as_another_user(self):
        # REGISTER 1st user
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")
        login_data = {
            'email': email,
            'password': password
        }

        # LOGIN 1st user
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # REGISTER 2nd user
        register_data = self.prepare_registration_data(username="user2")
        response3 = MyRequests.post("/user", data=register_data)
        Assertions.assert_code_status(response3, 200)
        Assertions.assert_json_has_key(response3, "id")
        username2 = register_data['username']
        user_id2 = self.get_json_value(response3, "id")

        # DELETE 2nd user
        response4 = MyRequests.delete(f"/user/{user_id2}",
                                    headers={"x-csrf-token": token},
                                    cookies={"auth_sid": auth_sid},
                                    )
        Assertions.assert_code_status(response4, 200)

        # GET 2nd user
        response5 = MyRequests.get(f"/user/{user_id2}")
        Assertions.assert_code_status(response5, 200)
        Assertions.assert_json_value_by_name(
            response5,
            "username",
            username2,
            f"User with username {username2} doesn't exist (was deleted)"
        )