import time
import requests
import json

# создание задачи. Вызов метода без get-параметра token
response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
#print(response.text)
obj = json.loads(response.text)
token = obj["token"]
print(token)
seconds = obj["seconds"]
print(seconds)

# один запрос с token до того, как задача готова
response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": token})
# print(response.text)
obj = json.loads(response.text)
status = obj["status"]
print("Статус:", status)

# ожидание нужного кол-ва секунд
if status == "Job is NOT ready":
    time.sleep(seconds)

# запрос с token после того, как задача готова
response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": token})
obj = json.loads(response.text)
status = obj["status"]
print("Статус:", status)
if status == "Job is ready":
    result = obj["result"]
    print("Результат:", result)
else:
    print("Задача еще не готова!")
