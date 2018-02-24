import psycopg2
import matplotlib.pyplot as plt
import numpy as np
import itertools
import random
from collections import Counter, defaultdict
import gender_guesser.detector as gender
import csv

hostname = 'localhost'
username = 'postgres'
password = 'kiva123'
database = 'kivadatabase'

name_list = []
counter = 0
unknown = 0
female = 0
male = 0

d = gender.Detector()

def getRewiringdata(conn):
    cur = conn.cursor()    
    cur.execute("""SELECT 
				    lenders_name,
				    borrowers_genders
				    FROM flows_data_notnull
                    where borrowers_genders is not null AND lenders_country = 'US'
				    order by lenders_name, borrowers_genders
					""")
	
    with open('name-gender-dict.csv', 'w') as myFile:
	    for lenders_name, borrowers_genders in cur.fetchall():
	    	if lenders_name not in name_list:
			    try:
			    	global counter, female, male, unknown
			    	lenders_name = lenders_name.title().partition(' ')[0]
			    	lender_gender = d.get_gender(lenders_name)

			    	counter = counter + 1
			    	print(lenders_name + ": " + lender_gender)

			    	if lender_gender == 'female' or lender_gender == 'mostly_female':
			    		female = female + 1
			    		myData = [lenders_name, lender_gender]
				    	writer = csv.writer(myFile)
				    	writer.writerow(myData)

			    	elif lender_gender == 'male' or lender_gender == 'mostly_male':
			    		male = male + 1
			    		myData = [lenders_name, lender_gender]
				    	writer = csv.writer(myFile)
				    	writer.writerow(myData)

			    	else :
			    		unknown = unknown + 1
			    	name_list.append(lenders_name)
			    except:
			    	pass
    print('Total of: ', counter, '||Female: ', female, '|| Male: ', male , '|| Unknown:', unknown)    	

myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database)
getRewiringdata(myConnection)