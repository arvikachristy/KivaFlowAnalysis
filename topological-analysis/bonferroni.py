import psycopg2
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
import scipy
from scipy.stats.stats import pearsonr, kendalltau
from scipy.stats import hypergeom

hostname = 'localhost'
username = 'postgres'
password = 'kiva123'
database = 'kivadatabase'


hypergeo_store = []
n_counter = 0 #how many w in this whole flow
l_counter = 0 #number of distinct pair

bonferroni = 0
survived_n = 0

def getLenderCount(conn):
    cur = conn.cursor()
    counter = 0
    cur.execute("""SELECT 
					country_from, country_to, n_l, n_r, flow
					from full_data_bonferroni
					""")
    for country_from, country_to, n_l, n_r, flow in cur.fetchall():
    	global n_counter, l_counter
    	n_counter = n_counter + float(flow)
    	l_counter = l_counter + 1
    	hypergeo_store.append([country_from, country_to, float(n_l), float(n_r), float(flow)])

def hypergeo_cal(country_from, country_to, n_l, n_r, flow):
	prb = hypergeom.sf(flow, n_counter, n_l, n_r)
	if prb<bonferroni: #if less then survived
		global survived_n
		survived_n = survived_n + 1
	# print(country_from, ',', country_to,',', prb,',', n_counter,',' ,l_counter)

def bonferroni_cal(l_val):
	global bonferroni
	bonferroni = 0.01/l_val

myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database)
getLenderCount(myConnection)

for item in hypergeo_store:
	hypergeo_cal(item[0], item[1], item[2], item[3], item[4])
	bonferroni_cal(l_counter)
	
print('No of survived pair:', survived_n ,'with:',(survived_n/l_counter)*100, '%')

myConnection.close()