from flask import Flask, url_for, request, make_response
from flask_sqlalchemy import SQLAlchemy
import datetime
import json

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class TH(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float, unique=False)
    humidity = db.Column(db.Float, unique=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
    
    def __init__(self, temperature, humidity):
        self.temperature = temperature
        self.humidity = humidity

    def __repr__(self):
        return '<temperature: %0.1f  humidity: %0.1f>' % (self.temperature, self.humidity)

@app.route('/')
def index():
    return makeResponse('Hello World!')

@app.route('/lot/th/')
def queryTHRecords():
    temp = []    
    records = db.session.query(TH).order_by(TH.created_date.desc()).limit(20)
    for th in records:
        temp.append({'temperature': th.temperature, 'humidity': th.humidity, 'created_date': str(th.created_date)})
    return  makeResponse(json.dumps(temp))

@app.route('/lot/th/add/<t>/<h>')
def addNewTHRecord(t, h):
    record = TH(t, h)
    db.session.add(record)
    db.session.commit()
    return makeResponse('success')

def makeResponse(content: str):
    res = make_response(content)
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'GET'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return res

if __name__ == '__main__':
    app.run()
