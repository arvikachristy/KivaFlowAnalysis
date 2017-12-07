import psycopg2
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np

hostname = 'localhost'
username = 'postgres'
password = 'kiva123'
database = 'kivadatabase'

plot_gravity = []
weight_flow = []
country_A =[]
country_B=[]

def reg_predictions(X, intercept, slope): 
    return ((slope*X) + intercept)

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
    
    # formula for w0
    slope = (sum_xy - (sum_x*sum_y)/n)/(sum_xx - (sum_x*sum_x)/n)
    
    # formula for w1
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
        #to make sure no double flows exist, from 376 to 91 flows
        if (country_from not in country_B and country_to not in country_A):
            counter +=1
            country_A.append(country_from)
            country_B.append(country_to)
            country_from, country_to, gravModel(float(kmdist),float(forward_count), float(backward_count), float(lenders_population), float(loans_population))

def doQuery2(conn):
    cur = conn.cursor()
    print ('STARTING SECOND BATCH')
    countering = 0
    cur.execute("""SELECT
                    country_from, country_to, kmdist, flow_country_count, lenders_population, loans_population
                    FROM country_weight_flow
                """)
    for country_from, country_to, kmdist, flow_country_count, lenders_population, loans_population in cur.fetchall():
        #to make sure no double flows exist, from 376 to 91 flows
        if (country_from not in country_B and country_to not in country_A):
            countering +=1
            # print (countering) 
            country_A.append(country_from)
            country_B.append(country_to)
            country_from, country_to, gravModel(float(kmdist),float(flow_country_count), 0, float(lenders_population), float(loans_population))
    
         
def gravModel(distance, forward_count, backward_count, populationA, populationB):
    weight = forward_count + backward_count
    gravity = (populationA * populationB)/(distance*distance)
    plot_gravity.append(gravity)
    weight_flow.append(weight)
    # plot result
    return gravity

print("Using psycopg2…")
myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
# doQuery(myConnection)
doQuery2(myConnection)

##Plotting the graph to matplot

# print(sorted(weight_flow))

# print(len(weight_flow))
for p in weight_flow:
    if (p <1):
        print("helo")

x = np.log(weight_flow)
y = np.log(plot_gravity)
plt.ylabel('Kiva 2 Countries Flow')
plt.xlabel('Population/distance')
# plt.plot(x, y, 'ro')

intercept, slope = simple_linear_regression(x, y)

print ('Intercept: %.2f, Slope: %.2f' % (intercept, slope))

line_x = np.array([x/10. for x in range(100)])
line_y = reg_predictions(line_x, intercept, slope)
plt.plot(x, y, 'ro', line_x, line_y, '-')

# fig, ax = plt.subplots()
# fit = np.polyfit(x, y, deg=1)
# ax.plot(x, fit[0] * x + fit[1], color='blue')
# ax.scatter(x, y)
# fig.text(0.5, 0.04, 'Population/Distance', ha='center', va='center')
# fig.text(0.06, 0.5, 'Kiva 2 Countries Flow', ha='center', va='center', rotation='vertical')

plt.show()

myConnection.close()
