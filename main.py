# from json.decoder import JSONDecodeError
import requests

response = requests.post("https://playground.learnqa.ru/api/get_301", allow_redirects=True)
print(response.status_code)
first_response = response.history[0]
second_response = response
print(first_response.url)
print(second_response.url)
# print(response.text)


