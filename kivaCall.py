import psycopg2
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np

hostname = 'localhost'
username = 'postgres'
password = 'kiva123'
database = 'kivadatabase'

def doQuery(conn):
    cur = conn.cursor()

    cur.execute("""SELECT DISTINCT lenders_country,loans_country_code,count(loans_country_code) as counter
					FROM flows_data 
					GROUP BY lenders_country, loans_country_code
					ORDER BY lenders_country, loans_country_code
					""" 
					)

    fig, ax = plt.subplots()

    min_val, max_val = 0, 195

    intersection_matrix = np.random.randint(0, 195, size=(max_val, max_val))

    ax.matshow(intersection_matrix, cmap=plt.cm.Blues)

    lenders_to_numbers={}

    loans_to_numbers = {}

    dex = 0

    index = 0

    lenders_ar=[]
    loans_ar=[]

    lenCount = 0
    loanCount = 0

    for lenders_country, loans_country_code, counter in cur.fetchall():        
        if lenders_country not in lenders_ar:
            lenders_ar.insert(index,lenders_country)
            lenCount += 1
        if loans_country_code not in loans_ar:
            loans_ar.insert(dex,loans_country_code)
            loanCount += 1            

    # print(lenders_ar[1])

    for lenders in lenders_ar:
        if lenders not in lenders_to_numbers:
            lenders_to_numbers[lenders]=index
            index += 1

    for loans in loans_ar:
        if loans not in loans_to_numbers:
            loans_to_numbers[loans]=dex
            dex += 1            

    for i in lenders_to_numbers:
    	for j in loans_to_numbers:
        	c = intersection_matrix[j,i]
        	ax.text(i, j, str(c), va='center', ha='center')            		
        
    print(len(loans_to_numbers))
# def gravModel(countryA, countryB, weight):


print("Using psycopg2…")
myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
doQuery(myConnection)
myConnection.close()
