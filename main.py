from json.decoder import JSONDecodeError
import requests

response = requests.get("https://playground.learnqa.ru/api/get_text")
print(response.text)
try:
    parced_response_text = response.json()
    print(parced_response_text)
except JSONDecodeError:
    print("Response is not a JSON format")

