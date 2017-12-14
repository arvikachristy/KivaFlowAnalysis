import psycopg2
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
import scipy
from scipy.stats.stats import pearsonr,spearmanr

hostname = 'localhost'
username = 'postgres'
password = 'kiva123'
database = 'kivadatabase'

plot_gravity = []
weight_flow = []
country_map=[]

def reg_predictions(X, intercept, slope): 
    return ((slope*X) + intercept)

def vertical_offset(slope, intercept, x, y):
    #x is flow y is gravity
    y1 = intercept + (slope * x) #w0 + w1*x
    v_offset = y1 - y
    return v_offset

def simple_linear_regression(X, y):
    '''
    Returns slope and intercept for a simple regression line
        X - input data
        y - output data
        
    outputs - floats
    '''
    # initial sums
    n = float(len(X))
    sum_x = X.sum()
    sum_y = y.sum()
    sum_xy = (X*y).sum()
    sum_xx = (X**2).sum()
    
    # formula for w1
    slope = (sum_xy - (sum_x*sum_y)/n)/(sum_xx - (sum_x*sum_x)/n)
    
    # formula for w0
    intercept = sum_y/n - slope*(sum_x/n)
    
    return (intercept, slope)


def doQuery(conn):
    cur = conn.cursor()
    counter = 0
    cur.execute("""SELECT 
                    country_from, country_to, forward_count, backward_count, kmdist, lenders_population, loans_population
					FROM forward_backward_flow
					""")

    for country_from, country_to, forward_count, backward_count, kmdist, lenders_population, loans_population in cur.fetchall():
        if (all(set((country_from, country_to)) != set(cmap[:2]) for cmap in country_map)):
            gravModel(country_from, country_to, float(kmdist),float(forward_count), float(backward_count), float(lenders_population), float(loans_population))            

def doQuery2(conn):
    cur = conn.cursor()
    print ('STARTING SECOND BATCH')
    cur.execute("""SELECT
                    country_from, country_to, kmdist, flow_country_count, lenders_population, loans_population
                    FROM country_weight_flow
                """)
    for country_from, country_to, kmdist, flow_country_count, lenders_population, loans_population in cur.fetchall():
        if (all(set((country_to, country_from)) != set(cmap[:2]) for cmap in country_map)):
            if (all(set((country_from, country_to)) != set(cmap[:2]) for cmap in country_map)):
                gravModel(country_from, country_to, float(kmdist),float(flow_country_count), 0, float(lenders_population), float(loans_population))

def gravModel(country_from, country_to, distance, forward_count, backward_count, populationA, populationB):
    weight = forward_count + backward_count
    gravity = (populationA * populationB)/(distance*distance)
    plot_gravity.append(gravity)
    weight_flow.append(weight)
    country_map.append([country_from, country_to, distance, gravity, weight])
    return gravity

print("Using psycopg2…")
myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
doQuery(myConnection)
doQuery2(myConnection)

#Plotting the graph to matplot
x = np.log(weight_flow)
y = np.log(plot_gravity)
plt.xlabel('Kiva 2 Countries Flow (log)')
plt.ylabel('Population/distance (log)')

#Getting slope and Intercept value
intercept, slope = simple_linear_regression(x, y)
print ('Intercept: %.2f, Slope: %.2f' % (intercept, slope))
print(len(weight_flow), 'weight_flow')
print(len(plot_gravity), 'grav_flow')

text_file = open("Output.txt", "w")

for item in country_map:
    offset = vertical_offset(slope, intercept, np.log(item[4]), np.log(item[3]))
    offset_storage.append(offset)
    text_file.write("{} {} {} {} {} {}\n".format(*item, offset))

line_y = reg_predictions(x, intercept, slope)
plt.plot(x, y, 'ro', x, line_y, '-')

plt.show()

text_file.close()

myConnection.close()