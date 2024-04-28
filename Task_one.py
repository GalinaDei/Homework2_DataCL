'''Урок 2. Парсинг HTML. BeautifulSoup
Выполнить скрейпинг данных в веб-сайта http://books.toscrape.com/ 
и извлечь информацию о всех книгах на сайте во всех категориях: 
название, цену, количество товара в наличии (In stock (19 available)) в формате integer, описание.

Затем сохранить эту информацию в JSON-файле.'''

from bs4 import BeautifulSoup
import requests
import urllib.parse
import pandas as pd
import json

url = 'http://books.toscrape.com/'
url1 = 'http://books.toscrape.com/catalogue/'
next_page_link = ''

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
next_page_link = soup.find('li', ('class', 'next')).find('a').get('href')
links = []
for c in soup.find_all('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'}):
    href = c.find('a')
    if href:
        links.append(href.get('href'))

abs_links = [urllib.parse.urljoin(url, link) for link in links]
    
headers = ["Name", "Price", "In stock", "Description"]
data = []
for link in abs_links:
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    row_dict = {}
    for i in range(len(headers)):
        row_dict[headers[0]] = soup.find('div', {'class': 'col-sm-6 product_main'}).find('h1').text
        row_dict[headers[1]] = soup.find('div', {'class': 'col-sm-6 product_main'}).find('p').text
        text = (soup.find('div', {'class': 'col-sm-6 product_main'}).find('p',{'class': 'instock availability'}).text.strip())
        row_dict[headers[2]] = int(text[text.find("(")+1:text.find(")")].split()[0])
        all_items = soup.find_all('p')
        for item in all_items:
            if not item.attrs:
                row_dict[headers[3]] = item.text
        
        
    data.append(row_dict)

df = pd.DataFrame(data)
print(df.tail(5))

with open('box_office_data.json', 'w') as f:
    json.dump(data, f)

print(next_page_link)
url = url + next_page_link
print(url)

while True:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    next_page_link = soup.find('li', ('class', 'next')).find('a').get('href')
    links = []
    for c in soup.find_all('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'}):
        href = c.find('a')
        if href:
            links.append(href.get('href'))
            
    abs_links = [urllib.parse.urljoin(url, link) for link in links]

    data = []
    for link in abs_links:
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        row_dict = {}
        for i in range(len(headers)):
            row_dict[headers[0]] = soup.find('div', {'class': 'col-sm-6 product_main'}).find('h1').text
            row_dict[headers[1]] = soup.find('div', {'class': 'col-sm-6 product_main'}).find('p').text
            text = (soup.find('div', {'class': 'col-sm-6 product_main'}).find('p',{'class': 'instock availability'}).text.strip())
            row_dict[headers[2]] = int(text[text.find("(")+1:text.find(")")].split()[0])
            all_items = soup.find_all('p')
            for item in all_items:
                if not item.attrs:
                    row_dict[headers[3]] = item.text
            
            
        data.append(row_dict)

    df = pd.DataFrame(data)
    print(df.tail(5))

    with open('box_office_data.json', 'a') as f:
        json.dump(data, f)


    url = url1 + next_page_link
    print(url)
    print(next_page_link)

    if not next_page_link:
        break
    
