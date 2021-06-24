# print("Hello, world!")
import requests

# payload = {"name": "User"}
# response = requests.get("https://playground.learnqa.ru/api/hello", params=payload)
# parsed_response_text = response.json()
# print(parsed_response_text["answer"])

response = requests.get("https://playground.learnqa.ru/api/get_text")
print(response.text)
parsed_response_text = response.json()
print(parsed_response_text)



