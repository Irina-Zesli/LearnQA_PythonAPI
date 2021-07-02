import requests

class TestReqCookie:
    def test_req_cookie(self):
        url = "https://playground.learnqa.ru/api/homework_cookie"
        response = requests.get(url)
        assert response.status_code == 200, "Wrong response code"
        response_cookie = dict(response.cookies)
        # print(response.cookies) #чтобы узнать, что {'HomeWork': 'hw_value'}
        assert 'HomeWork' in response_cookie, "There is no cookie 'HomeWork' in the response"
        assert response_cookie['HomeWork'] == 'hw_value', "Actual value of cookie in the response is not correct"

