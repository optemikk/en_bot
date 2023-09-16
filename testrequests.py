import requests

resp = requests.get('https://kodik.info/serial/51955/9bab625cac205b20d165454f8e30195d/720p')
print(resp.content)