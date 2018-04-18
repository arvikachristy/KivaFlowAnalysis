###############################################################################
# GENDER GUESSER SCRIPT - using basic library (Advanced is in another script)
# -----------------------------------------------------------------------------
# This script is made AFTER creating the gender dictionary on psql
# We use this script to fill the rest of the gender-less names on your database
# Current Level: Individual to Individual (Philliphines borrowers Network)
###############################################################################
import psycopg2
import matplotlib.pyplot as plt
import numpy as np
import itertools
import random
from collections import Counter, defaultdict
import csv
import gender_guesser.detector as gender

hostname = 'localhost'
username = 'postgres'
password = 'kiva123'
database = 'kivadatabase'

name_list = []
counter = 0
unknown = 0
female = 0
male = 0
group = 0
weird_fem = 0
weird_mal = 0
weird_unk = 0
disp = 0

d = gender.Detector()

def getRewiringdata(conn):
    cur = conn.cursor()    
    cur.execute("""SELECT
					lenders_name,
					lender_gender,
					borrowers_genders
					from ph_rewiring_data
					""")
    with open('name-gender-dict.csv', 'w', newline='') as myFile:
	    for lenders_name, lender_gender, borrowers_genders in cur.fetchall():
		    try:
		    	global counter, female, male, unknown, group
		    	lenders_name = lenders_name.title()
		    	counter = counter + 1
		    	if " + " in lenders_name or " & " in lenders_name or " And " in lenders_name or "/" in lenders_name:
		    		group = group + 1
		    		myData = [lenders_name, 'group', borrowers_genders]
			    	writer = csv.writer(myFile)
			    	writer.writerow(myData)		
		    	elif lender_gender == 'female':
		    		female = female + 1
		    		myData = [lenders_name, 'female', borrowers_genders]
			    	writer = csv.writer(myFile)
			    	writer.writerow(myData)		    		
		    	elif lender_gender == 'male':
		    		male = male + 1
		    		myData = [lenders_name, 'male', borrowers_genders]
		    		writer = csv.writer(myFile)
		    		writer.writerow(myData)
		    	else:
		    		unknown = unknown + 1
		    		lenders_name = lenders_name.split(' ', 1)[0]
		    		cur_lender_gender = d.get_gender(lenders_name)
		    		global weird_fem,weird_mal, weird_unk
		    		if cur_lender_gender == 'female' or cur_lender_gender == 'mostly_female':
		    			weird_fem = weird_fem + 1
		    			myData = [lenders_name, 'female', borrowers_genders]
		    			writer = csv.writer(myFile)
		    			writer.writerow(myData)
		    		elif cur_lender_gender == 'male' or cur_lender_gender == 'mostly_male':
		    			weird_mal = weird_mal + 1
		    			myData = [lenders_name, 'male', borrowers_genders]
		    			writer = csv.writer(myFile)
		    			writer.writerow(myData)
		    		else:
		    			weird_unk = weird_unk + 1
		    			myData = [lenders_name, 'unknown', borrowers_genders]
		    			writer = csv.writer(myFile)
		    			writer.writerow(myData)
		    except:
		    	global disp
		    	disp = disp + 1
		    	pass
    print('Total of: ', counter, '||Female: ', female, '|| Male: ', male , '|| Group:', group, '|| Unknown:', unknown)    	
    print('||weirdFemale: ', weird_fem, '|| Male: ', weird_mal ,'|| weirdUnknown:', weird_unk)
    print('Total passed', disp)   	

myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database)
getRewiringdata(myConnection)