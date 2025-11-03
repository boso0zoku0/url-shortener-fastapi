import requests

url = "https://x.testtty.ru/tasks/list"

# Куки
cookies = {
    "session": "bf4b662b25d6ba2cc9dcf9376de9f3cfa334db57b99d3d9f9a96dc17121db802"
}

# Отсылаем GET-запрос с указанным cookie
response = requests.get(url, cookies=cookies)

# Проверяем ответ
print(response.status_code)
print(response.text)
