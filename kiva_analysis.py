import psycopg2
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np

##DONT USE

hostname = 'localhost'
username = 'postgres'
password = 'kiva123'
database = 'kivadatabase'

plot_gravity = []
weight_flow = []
country_A =[]
country_B=[]
country_dist=[]

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
                    country_from, country_to, flow, distance, gravity
					FROM analysis_data
					""")

    for country_from, country_to, flow, distance, gravity in cur.fetchall():
        country_A.append(country_from)
        country_B.append(country_to)
        country_dist.append(distance)
        plot_gravity.append(float(gravity))
        weight_flow.append(float(flow))

# def gravModel(gravity_country, flow):
#     plot_gravity.append(gravity_country)
#     weight_flow.append(flow)

print("Using psycopg2…")
myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
doQuery(myConnection)

#Plotting the graph to matplot
x = np.log(weight_flow)
y = np.array(plot_gravity)
# print(plot_gravity)
plt.xlabel('Kiva 2 Countries Flow (log)')
plt.ylabel('Population/distance (log)')

#Getting slope and Intercept value
intercept, slope = simple_linear_regression(x, y)
print ('Intercept: %.2f, Slope: %.2f' % (intercept, slope))

#Getting the vertical offset on the table
for a, b, c, d, e, weight_flow in zip(country_A, country_B, x, y, country_dist, weight_flow):
    offset = vertical_offset(slope, intercept, c, d)
    #print (a, b, c, d, offset) #display country from, country to, 
    print(a, ",", b, ",", offset, ",",e, ",", weight_flow,"," , c)
    # print(len(weight_flow))

line_x = np.array([x/10. for x in range(100)])
line_y = reg_predictions(line_x, intercept, slope)
plt.plot(x, y, 'ro', line_x, line_y, '-')

plt.show()

myConnection.close()
