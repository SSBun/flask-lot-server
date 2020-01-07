from flask import Flask, url_for, request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class TH(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float, unique=False)
    humidity = db.Column(db.Float, unique=False)
    
    def __init__(self, temperature, humidity):
        self.temperature = temperature
        self.humidity = humidity

    def __repr__(self):
        return '<temperature: %0.1f  humidity: %0.1f>' % (self.temperature, self.humidity)

@app.route('/')
def index():
    return "Hello Worlddadccd!"

@app.route('/lot/th/')
def queryTHRecords():
    temp = []
    for th in TH.query.all():
        temp.append({'temperature': th.temperature, 'humidity': th.humidity})
    return json.dumps(temp)

@app.route('/lot/th/add/<float:t>/<float:h>')
def addNewTHRecord(t, h):
    record = TH(t, h)
    db.session.add(record)
    db.session.commit()
    return 'add record success'


if __name__ == '__main__':
    app.run()
