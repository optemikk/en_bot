from requests import Response
from requests_html import HTMLSession
from bs4 import BeautifulSoup

session = HTMLSession()
response = session.get('https://youla.ru/izhevsk?q=iphone')
response.html.render()
# soup = BeautifulSoup(response.text, 'html.parser')
# print(soup)
print(response.json()[0]['html'])