""" This is the Kiva 'adapter'.

This is where you would fetch data from Kiva. Think requets.get('http://api.kiva.com').

"""

import requests

def get():
    response = requests.get('http://api.kivaws.org/v1/loans/newest.json')
    return response.json()['loans']

