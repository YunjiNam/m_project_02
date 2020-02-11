import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('http://chcgv.tving.com/chcgv/schedule?startDate=20200203#' ,headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

chcgv_li = soup.select('.contentInnerWrap > section > div.scheduler > table > tbody > tr')

rank = 1
for c_movie in chcgv_li:
    a_tag = c_movie.select_one('td.programInfo > div > div.program')
    if a_tag is not None:
        title = a_tag.text.strip()
        w_time = c_movie.select_one('td.programInfo > div > em.airTime').text.strip()
        rating = c_movie.select_one('td.rating > span').text
        print(rank,title,w_time,rating)
        doc = {
            'rank' : rank,
            'title' : title,
            'w_time' : w_time,
            'rating' : rating
        }
        db.chcgv_li.insert_one(doc)
        rank += 1



