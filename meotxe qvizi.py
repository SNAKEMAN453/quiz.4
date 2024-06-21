import csv
import sqlite3
import requests
from bs4 import BeautifulSoup

url = 'https://tabula.ge/ge'
response = requests.get(url)
info = BeautifulSoup(response.text, 'html.parser')
data = info.find('div', class_='NewsItemList_newsItemListContainer__1WjYx')
table_items = data.find_all('div', class_='news-item-list-item')
conn = sqlite3.connect("tabula.sqlite")
cursor = conn.cursor()



for index, item in enumerate(table_items, start=1):
    title = item.find('img', class_='Thumbnail_thumbnail__4GIBv').attrs['alt']
    image = item.find('img', class_='Thumbnail_thumbnail__4GIBv').attrs['src']
    time = item.find('time').attrs['title']
    info = f'{index}. {title}, {time}'


    cursor.execute('''CREATE TABLE IF NOT EXISTS News
                   (ID INTEGER PRIMARY KEY AUTOINCREMENT ,
                   TITLE TEXT,
                   TIME TIME,
                   COVER TEXT)''')

    cursor.execute('INSERT INTO News (TITLE, TIME, COVER) VALUES (?,?,?)', (title, time, image))
    conn.commit()
