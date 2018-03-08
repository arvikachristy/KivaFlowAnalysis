""" This is the Kiva 'adapter'.

This is where you would fetch data from Kiva. Think requets.get('http://api.kiva.com').

"""

import requests

def get():
    response = requests.get('C:\Users\User\Documents\YearFourUCL-Vika\FinalYearProject-Kiva\kiva_ds_json\loans.json')
    return response.json()['loans']

