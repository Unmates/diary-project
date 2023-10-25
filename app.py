import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from datetime import datetime

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client= MongoClient("mongodb://farelli:shakti@ac-mrep1ay-shard-00-00.kxxqxff.mongodb.net:27017,ac-mrep1ay-shard-00-01.kxxqxff.mongodb.net:27017,ac-mrep1ay-shard-00-02.kxxqxff.mongodb.net:27017/?ssl=true&replicaSet=atlas-afnrt3-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client["dbsparta"]

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    diary_list = list(db.diary.find({},{'_id': False}))
    return jsonify({'diary':diary_list})

@app.route('/diary', methods=['POST'])
def save_diary():
    today = datetime.now()
    date = today.strftime('%Y-%m-%d %H-%M-%S')
    time = today.strftime('%Y-%m-%d')

    file_receive = request.files['file_give']
    file_ex = file_receive.filename.split('.')[-1]
    filename = f'static/img{date}.{file_ex}'
    file_receive.save(filename)

    profile_receive = request.files['profile_give']
    profile_ex = profile_receive.filename.split('.')[-1]
    profilename = f'static/prf{date}.{profile_ex}'
    profile_receive.save(profilename)

    tittle_receive = request.form['tittle_give']
    content_receive = request.form['content_give']

    doc={
        'file' : filename,
        'profile' : profilename,
        'tittle' : tittle_receive,
        'content' : content_receive,
        'time' : time,
    }
    db.diary.insert_one(doc)
    return jsonify({'msg': 'POST request complete!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
  