import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

class TestUserEdit(BaseCase):

    def setup(self):
        # REGISTER 1st user
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        self.email = register_data['email']
        self.first_name = register_data['firstName']
        self.password = register_data['password']
        self.user_id = self.get_json_value(response1, "id")
        self.username = register_data['username']
        self.login_data = {
            'email': self.email,
            'password': self.password
        }

    def test_edit_just_created_user(self):

        #LOGIN 1st user
        response2 = MyRequests.post("/user/login", data=self.login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #EDIT 1st user
        new_name = "changed_name"

        response3 = MyRequests.put(f"/user/{self.user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"firstName": new_name}
                                 )

        Assertions.assert_code_status(response3, 200)

        #GET 1st user

        response4 = MyRequests.get(f"/user/{self.user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
                                 )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            f"Wrong name of the user after edit"
        )

    def test_edit_not_auth_user(self):
        #EDIT 1 st user
        new_username = "changed_name"
        response2 = MyRequests.put(f"/user/{self.user_id}", data={"username": new_username})
        Assertions.assert_code_status(response2, 400)
        #print(response2.status_code)
        #print(response2.content)
        Assertions.assert_content(response2, "Auth token not supplied")

        # GET 1st user

        response3 = MyRequests.get(f"/user/{self.user_id}")

        Assertions.assert_json_value_by_name(
            response3,
            "username",
            self.username,
            f"Username shouldn't have changed"
        )


    def test_edit_auth_as_another_user(self):

        # LOGIN 1st user

        response2 = MyRequests.post("/user/login", data=self.login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # REGISTER 2nd user
        register_data = self.prepare_registration_data(username="user2")
        response3 = MyRequests.post("/user", data=register_data)
        Assertions.assert_code_status(response3, 200)
        Assertions.assert_json_has_key(response3, "id")

        email2 = register_data['email']
        first_name2 = register_data['firstName']
        password2 = register_data['password']
        user_id2 = self.get_json_value(response3, "id")
        username2 = register_data['username']

        # EDIT 2nd user
        new_username = "changed_username"
        new_firstName = "changed_firstName"

        response3 = MyRequests.put(f"/user/{user_id2}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={
                                    "username": new_username,
                                    "firstName": new_firstName
                                 }
                                 )

        Assertions.assert_code_status(response3, 200)

        # LOGIN 2nd user
        login_data2 = {
            'email': email2,
            'password': password2
        }

        response4 = MyRequests.post("/user/login", data=login_data2)
        auth_sid2 = self.get_cookie(response4, "auth_sid")
        token2 = self.get_header(response4, "x-csrf-token")

        # GET 2nd user

        response5 = MyRequests.get(f"/user/{user_id2}",
                                 headers={"x-csrf-token": token2},
                                 cookies={"auth_sid": auth_sid2}
                                 )

        Assertions.assert_json_value_by_name(
            response5,
            "username",
            username2,
            f"Username shouldn't have changed"
        )
        Assertions.assert_json_value_by_name(
            response5,
            "firstName",
            first_name2,
            f"firstName shouldn't have changed"
        )

    def test_edit_wrong_email(self):
        # LOGIN 1st user
        response2 = MyRequests.post("/user/login", data=self.login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT 1st user
        new_email = "changed_email"

        response3 = MyRequests.put(f"/user/{self.user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"email": new_email}
                                 )
        #print(response3.status_code)
        Assertions.assert_code_status(response3, 400)
        #print(response3.content)
        Assertions.assert_content(response3, "Invalid email format")

        # GET 1st user
        response4 = MyRequests.get(f"/user/{self.user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
                                 )
        #print(response4.text)
        Assertions.assert_json_value_by_name(
            response4,
            "email",
            self.email,
            f"email shouldn't have changed"
        )

    def test_edit_short_firstname(self):
        # LOGIN 1st user

        response2 = MyRequests.post("/user/login", data=self.login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT 2-st user

        new_firstName = "A"
        response3 = MyRequests.put(f"/user/{self.user_id}",
                                     headers={"x-csrf-token": token},
                                     cookies={"auth_sid": auth_sid},
                                     data={"firstName": new_firstName}
                                     )
        #print(response3.status_code)
        Assertions.assert_code_status(response3, 400)
        #print(response3.content)
        Assertions.assert_content(response3, '{"error":"Too short value for field firstName"}')

        # GET 1st user
        response4 = MyRequests.get(f"/user/{self.user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
                                 )
        #print(response4.text)
        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            self.first_name,
            f"firstName shouldn't have changed"
        )


