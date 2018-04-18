###############################################################################
# USA GENDER GUESSER SCRIPT - using basic library (Advanced is in another script)
# -----------------------------------------------------------------------------
# This script is made to create the GENDER DICTIONARY based on lender's name and 
# import it to a csv file.
# In order to do so, we use a python library called gender guesser
# While not optimal, this script can be combined with hitting free API to guess 
# those that's still unknown.
# Level: Individual to Individual (USA Network)
###############################################################################

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
				    DISTINCT on (lenders_name)
                    lenders_name,
				    borrowers_genders
				    FROM flows_data_notnull
                    where borrowers_genders is not null AND lenders_country = 'US'
				    order by lenders_name, borrowers_genders
					""")
	
    with open('name-gender-dict.csv', 'w') as myFile:
	    for lenders_name, borrowers_genders in cur.fetchall():
		    try:
		    	global counter, female, male, unknown
		    	lenders_name = lenders_name.title().partition(' ')[0].replace(',','')
		    	lender_gender = d.get_gender(lenders_name)
		    	counter = counter + 1
		    	if lenders_name not in name_list:

			    	print(lenders_name + ": " + lender_gender)

			    	if lender_gender == 'female' or lender_gender == 'mostly_female':
			    		female = female + 1
			    		myData = [lenders_name, 'female']
				    	writer = csv.writer(myFile)
				    	writer.writerow(myData)

			    	elif lender_gender == 'male' or lender_gender == 'mostly_male':
			    		male = male + 1
			    		myData = [lenders_name, 'male']
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