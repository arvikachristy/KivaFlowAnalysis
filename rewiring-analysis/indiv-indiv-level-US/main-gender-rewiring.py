
###############################################################################
# GENDER REWIRING
# -----------------------------------------------------------------------------
# This is the script for gender rewiring, the result can be seen 
# clearly on the terminal after running it
# Level: indiv to Individual (Whole Network)
###############################################################################


import psycopg2
import matplotlib.pyplot as plt
import numpy as np
import scipy
import itertools
import random
from collections import Counter, defaultdict

hostname = 'localhost'
username = 'postgres'
password = 'kiva123'
database = 'kivadatabase'

lender_gender_list = []

gender_list=[] #F,F,M,M,F,F,M,G
total_everything = 0 #the overall total 

dic_gender = ['female', 'male', 'group']

finale = defaultdict(list)
after_cut = {}

def getRewiringdata(conn):
    cur = conn.cursor()    
    cur.execute("""SELECT lender_gender, borrowers_genders
					from ph_rewiring
					where lender_gender != 'unknown'
					""")
    for lender_gender, borrowers_genders in cur.fetchall():
    	global total_everything
    	total_everything = total_everything + 1 #counting overall row
    	if borrowers_genders == 'female' or borrowers_genders == 'male':
    		lender_gender_list.append(lender_gender)
    		gender_list.append(borrowers_genders)
    	else:
    		#If not male or female, name it group
    		lender_gender_list.append(lender_gender)
    		gender_list.append('group')

def getOriginal(country_l, sector_l):
	counts = Counter()

	for item in zip(country_l, sector_l):
		#key        = value
	    counts[item] += 1	
	return counts

def calPercentage(country_l, sector_l):
	counts = Counter()

	for item in zip(country_l, sector_l):
		#key        = value
	    counts[item] += 1

	for item in finale:
		if not item in counts:
			finale[item].append(0)
		else:
			finale[item].append(counts[item])

	return finale

def sortAndCut(list, iteration):
	cutsize = (iteration * 0.01)/2; 

	list.sort()	

	# print('Cutting this much item:', cutsize)

	list = list[int(cutsize):] #cut front

	list = list[:len(list)-int(cutsize)] #cut back
	
	# print(list)
	divList = [(x/ total_everything)*100 for x in list] #make it in percentage
	# print(divList)
	# print('after-------')

	return divList


def shufflingFunc():
	print('Starting the shuffle...')
	permutations = set() #The new mutated gender_list
	iteration = 1000

	while len(permutations) < iteration: #iterations???
		random.shuffle(gender_list)
		permutations.add(tuple(gender_list))

	print('Shuffle done...')

	counts = Counter() #only the one that got added
	combinations = set(itertools.product(lender_gender_list, dic_gender)) 

	for item in combinations:
		finale[item].append(counts[item])
		finale[item].pop(0)

	for permutation in permutations:
		occMap = calPercentage(lender_gender_list, permutation)

	print('Sorting and Cutting and Dividing...')
	after = {key: sortAndCut(value, iteration) for key, value in finale.items()}

	# for item in after:
	 	# print(str(item[0]),',', str(item[1]),',',(after[item]), '%')
	 	# print(str(item[0]),',', str(item[1]),',',(after[item][0]),',', (after[item][len(after[item])-1]), '%')	 
	return after	

myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database)
getRewiringdata(myConnection)

#Get Occurence original
oriMap = getOriginal(lender_gender_list, gender_list)

#Get Percentage original
for item in oriMap:
 	print(str(item[0]),',', str(item[1]),',',(oriMap[item]/total_everything)*100, '%')

#Reshuffling
rangeMap = shufflingFunc()
counter =0 
above=0
within=0
below=0
#Original vs Shuffling range
for item in oriMap:
	curRange = rangeMap.get(item) #get the range
	actual_no = (oriMap.get(item)/total_everything)*100
	counter = counter + 1
		
	if(actual_no > curRange[len(curRange)-1]):
		print (counter, ':', item, actual_no, ',' ,curRange[0], curRange[len(curRange)-1], '|| \x1b[6;30;42m' + 'Above the Range!' + '\x1b[0m')
		above = above + 1
	elif(actual_no < curRange[0]):
		print (counter, ':', item, actual_no, ',' ,curRange[0], curRange[len(curRange)-1], '|| \x1b[6;30;41m' + 'Below the Range!' + '\x1b[0m')		
		below = below + 1
	else:
		print(counter, ':', item, actual_no, ',' ,curRange[0], curRange[len(curRange)-1], '|| \x1b[6;30;47m' + 'Within the Range!' + '\x1b[0m')
		within = within + 1
print ('Total pairs:', counter)
print('Above: ', (above), '||Within: ', within, '|| Below: ', below)
print('Above: ', (above/counter)*100, '% ||Within: ', (within/counter)*100, '% || Below: ', (below/counter)*100, '%')
myConnection.close()