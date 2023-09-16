import requests
token = '6524572114:AAG4WfvdNkswheVRkIjg4ir0BWLc-MLgvKs'
chat_id = '972383332'
url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}>&text=Всем привет!'
response = requests.get(url=url)
print(response.json())