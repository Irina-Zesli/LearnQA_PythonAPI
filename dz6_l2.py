import requests

response = requests.post("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)
num_redir = len(response.history)
print("Количество редиректов: ", num_redir)
print("Итоговый url: ", response.history[num_redir-1].url)
