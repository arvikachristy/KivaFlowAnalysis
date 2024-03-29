###############################################################################
# Temporal REWIRING
# -----------------------------------------------------------------------------
# This is the script for temporal rewiring, the result can be seen 
# clearly on the terminal after running it
# Level: Country to Individual 
###############################################################################


import psycopg2
import matplotlib.pyplot as plt
import numpy as np
import scipy
import itertools
import random
from collections import Counter, defaultdict
from scipy.stats import hypergeom

hostname = 'localhost'
username = 'postgres'
password = 'kiva123'
database = 'kivadatabase'

countries_list = [] #AT, AU, AU, AU...

quarter_list=[] 
total_everything = 0 #the overall total 

dic_quarters = ['Q1', 'Q2', 'Q3']

finale = defaultdict(list)
after_cut = {}

def getQuarter(year):
	if   2006 <= year < 2010: return 'Q1'
	elif 2010 <= year < 2014: return 'Q2'
	elif 2014 <= year < 2018: return 'Q3'

def getRewiringdata(conn):
    cur = conn.cursor()    
    cur.execute("""SELECT 
				    lenders_country,
				    posted_time
				    FROM flows_data_notnull
                    where posted_time is not null
				    order by lenders_country, posted_time
					""")
    for lenders_country, posted_time in cur.fetchall():
    	global total_everything
    	total_everything = total_everything + 1 #counting overall row
    	year = int(posted_time[:4])
    	countries_list.append(lenders_country)
    	quarter_list.append(getQuarter(year))


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
	list = list[int(cutsize):] #cut front
	list = list[:len(list)-int(cutsize)] #cut back
	
	divList = [(x/ total_everything)*100 for x in list] #make it in percentage

	return divList


def shufflingFunc():
	print('Starting the shuffle...')
	permutations = set() #The new mutated quarter_list
	iteration = 10

	while len(permutations) < iteration: #iterations???
		random.shuffle(quarter_list)
		permutations.add(tuple(quarter_list))

	print('Shuffle done...')

	counts = Counter() #only the one that got added
	combinations = set(itertools.product(countries_list, dic_quarters)) 

	for item in combinations:
		finale[item].append(counts[item])
		finale[item].pop(0)

	for permutation in permutations:
		occMap = calPercentage(countries_list, permutation)

	print('Sorting and Cutting and Dividing...')
	after = {key: sortAndCut(value, iteration) for key, value in finale.items()}	 
	return after	

myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database)
getRewiringdata(myConnection)

#Get Occurence original
oriMap = getOriginal(countries_list, quarter_list)

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
		print (counter, ':', item, actual_no, '% ,' ,curRange[0], curRange[len(curRange)-1], '|| \x1b[6;30;42m' + 'Above the Range!' + '\x1b[0m')
		above = above + 1
	elif(actual_no < curRange[0]):
		print (counter, ':', item, actual_no, '% ,' ,curRange[0], curRange[len(curRange)-1], '|| \x1b[6;30;41m' + 'Below the Range!' + '\x1b[0m')		
		below = below + 1
	else:
		print(counter, ':', item, actual_no, '% ,' ,curRange[0], curRange[len(curRange)-1], '|| \x1b[6;30;47m' + 'Within the Range!' + '\x1b[0m')
		within = within + 1
print ('Total pairs:', counter)
print('Above: ', (above), '||Within: ', within, '|| Below: ', below)
print('Above: ', (above/counter)*100, '% ||Within: ', (within/counter)*100, '% || Below: ', (below/counter)*100, '%')
myConnection.close()