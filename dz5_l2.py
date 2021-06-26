from json.decoder import JSONDecodeError
import json

string_as_json = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},' \
                 '{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}'

try:
    obj = json.loads(string_as_json)
    key = "messages"
    if key in obj:
        obj1 = obj[key][1]
        key1 = "message"
        if key1 in obj1:
            print(obj1[key1])
        else:
            print(f"Ключа {key1} в JSON нет")
    else:
        print(f"Ключа {key} в JSON нет")

except JSONDecodeError:
    print("String is not a JSON format")
