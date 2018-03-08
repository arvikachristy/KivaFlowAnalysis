import psycopg2
import matplotlib.pyplot as plt
import numpy as np
import scipy
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

graph_dist = []
sorted_data = []
no=0

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
	prb = hypergeom.cdf(flow, n_counter, n_l, n_r)
	global no
	if prb<bonferroni: #if less then survived
		global survived_n
		survived_n = survived_n + 1
		graph_dist.append(prb) #applied the non random only
		sorted_data.append([country_from,country_to,prb, n_counter,l_counter, flow])

def bonferroni_cal(l_val):
	global bonferroni
	bonferroni = 0.001/l_val
	# print('bonferroni:', bonferroni, 'L:,', l_val)

myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database)
getLenderCount(myConnection)

for item in hypergeo_store:
	hypergeo_cal(item[0], item[1], item[2], item[3], item[4])
	bonferroni_cal(l_counter)
	
sorted_data.sort(key=lambda sorted_data: sorted_data[2])
for item in sorted_data:
	print(item[0], ',', item[1],',', item[2],',', item[3],',' , item[4], ',', item[5])


print('No of survived pair:', survived_n ,'with:',(survived_n/l_counter)*100, '%')


myConnection.close()
