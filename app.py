from flask import Flask, render_template, jsonify
app = Flask(__name__)

import datetime

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('movie_table_pro.html')

@app.route('/list', methods=['POST'])
def saving():
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('http://chcgv.tving.com/chcgv/schedule?startDate=20200203#' ,headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    chcgv_li = soup.select('.contentInnerWrap > section > div.scheduler > table > tbody > tr')

    dt = datetime.datetime.now()

    rank = 1
    for c_movie in chcgv_li:
        a_tag = c_movie.select_one('td.programInfo > div > div.program')
        if a_tag is not None:
            title = a_tag.text.strip()
            w_time = c_movie.select_one('td.programInfo > div > em.airTime').text.strip()
            rating = c_movie.select_one('td.rating > span').text
            r_time = c_movie.select_one('td.runningTime').text
            c_time = dt.strftime("%H시 %M분 %S")
            print(rank,title,w_time,rating,r_time)
            doc = {
                'rank' : rank,
                'title' : title,
                'w_time' : w_time,
                'rating' : rating,
                'r_time' : r_time,
                'c_time' : c_time
            }
            db.chcgv_li.insert_one(doc)
            rank += 1

            return jsonify({'result': 'success'})

@app.route('/list', methods=['GET'])
def view_lists():
    lists = list(db.chcgv_li.find({},{'_id':0}))
    return jsonify({'result':'success', 'lists':lists})

if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)



