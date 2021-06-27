import requests

print("1) Запрос любого типа без параметра method: ")
response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(response.text)
response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(response.text)
response = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(response.text)
response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(response.text)

print("2) Запрос не из списка:")
response = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(response.text)

print("3) Запрос с правильным значением параметра: ")
response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": 'GET'})
print(response.text)
response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": 'POST'})
print(response.text)
response = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": 'PUT'})
print(response.text)
response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": 'DELETE'})
print(response.text)

print("4) все возможные сочетания реальных типов запроса и значений параметра method.")
for method in 'GET', 'POST', 'PUT', 'DELETE':
    response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": method})
    print("Запрос GET с параметром ", method," : ", response.text)
    response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": method})
    print("Запрос POST с параметром ", method," : ", response.text)
    response = requests.put("https://playground.learnqa.ru/ajax/compare_query_type", data={"method": method})
    print("Запрос PUT с параметром ", method, " : ", response.text)
    response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": method})
    print("Запрос DELETE с параметром ", method, " : ", response.text)
    print("---------------------------------------------------------")

