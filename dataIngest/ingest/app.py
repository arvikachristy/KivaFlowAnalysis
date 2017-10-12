""" This is the app.

Here, you would set routes for your data ingest application. Routes should define the functionality. In this example, we have ways of getting data manually, and getting and updating a schedule. This schedule might be used at some later point to get data automatically (i.e. without a user having to specifically request it).

"""
import json

from flask import Flask, request, jsonify

import db
import kiva
import schedule
import schema

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    # response = urllib.request.urlopen('https://api.kivaws.org/v1/loans/newest.json')
    # res = response.read()
    # data = json.loads(res)
    return 'helloworld'

@app.before_first_request
def setup_database():
    db.setup()

@app.route('/data', methods=['GET'])
def get_data():
    data = kiva.get()
    transformedData = schema.transform(data)
    db.insert(transformedData)
    return ('',204)

@app.route('/schedule', methods=['GET', 'POST'])
def get_or_update_schedule():
    if request.method == 'GET':
        return schedule.get()

    if request.method == 'POST':
        return schedule.update()