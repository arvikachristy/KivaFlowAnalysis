###############################################################################
# Sector REWIRING
# -----------------------------------------------------------------------------
# This is the script for sector rewiring, the result can be seen 
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

original_sector_store = []
countries_list = [] #AT, AU, AU, AU...
sector_list = [] #FOOD, ARGI, ARGI, ARGI
total_everything = 0 #the overall total 

dic_sectors = ['Agriculture','Arts','Clothing','Construction','Education','Entertainment','Food','Health','Housing','Manufacturing','Personal Use','Retail','Services','Transportation','Wholesale']

finale = defaultdict(list)
after_cut = {}

def getRewiringdata(conn):
    cur = conn.cursor()    
    cur.execute("""SELECT 
				    lenders_country,
				    loans_sector
				    FROM flows_data_notnull
				    order by lenders_country, loans_sector
					""")
    for lenders_country, loans_sector in cur.fetchall():
    	global total_everything
    	total_everything = total_everything + 1 #counting overall row
    	countries_list.append(lenders_country)
    	sector_list.append(loans_sector)

def getOriginal(country_l, sector_l):
	counts = Counter()

	for item in zip(country_l, sector_l):
	    counts[item] += 1	
	return counts

def calPercentage(country_l, sector_l):
	counts = Counter()

	for item in zip(country_l, sector_l):
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
	permutations = set() #The new mutated sector_list
	iteration = 1000

	while len(permutations) < iteration: #iterations???
		random.shuffle(sector_list)
		permutations.add(tuple(sector_list))

	print('Shuffle done...')

	counts = Counter() #only the one that got added
	combinations = set(itertools.product(countries_list, dic_sectors)) 

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
oriMap = getOriginal(countries_list, sector_list)

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