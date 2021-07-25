import requests

class TestReqHeader:
    def test_req_header(self):
        url = "https://playground.learnqa.ru/api/homework_header"
        response = requests.get(url)
        response_headers = response.headers
        print(response_headers) # Чтобы узнать, что 'x-secret-homework-header': 'Some secret value'
        assert response.status_code == 200, "Wrong response code"
        assert 'x-secret-homework-header' in response_headers, "There is no header 'x-secret-homework-header' in the response"
        assert response_headers['x-secret-homework-header'] == 'Some secret value', "Actual value of header in the response is not correct"