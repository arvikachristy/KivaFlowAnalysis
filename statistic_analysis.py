#FOR ANALYSIS PURPOSES
import psycopg2
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
import scipy
from scipy.stats.stats import pearsonr, kendalltau

hostname = 'localhost'
username = 'postgres'
password = 'kiva123'
database = 'kivadatabase'


offset_store =[]
gdp_store = []
offset_abs_store = []
def doQuery(conn):
    cur = conn.cursor()
    counter = 0
    cur.execute("""SELECT 
                    country_from, country_to, offset_value, gdp_abs, offset_abs
					FROM analysis_data
					""")

    for country_from, country_to, offset_value, gdp_diff_abs, offset_abs in cur.fetchall():
    	offset_store.append(float(offset_value))
    	gdp_store.append(float(gdp_diff_abs))
    	offset_abs_store.append(float(offset_abs))
    print(len(offset_store))
    print(len(gdp_store))

myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database)
doQuery(myConnection)


print (kendalltau(np.array(offset_abs_store), np.array(gdp_store)))
print (pearsonr(np.array(offset_abs_store), np.array(gdp_store)))



myConnection.close()