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

def doQuery(conn):
    cur = conn.cursor()
    counter = 0

    ##THIS IS FOR THE ONE WHO HAS LEND TO EACH OTHER ONLY, THATS WHY ITS SO SMALL
    cur.execute("""SELECT 
                    country_from, country_to, forward_count, backward_count, kmdist, lenders_population, loans_population
					FROM forward_backward_flow
					"""
					)

    for country_from, country_to, forward_count, backward_count, kmdist, lenders_population, loans_population in cur.fetchall():
        #to make sure no double flows exist, from 376 to 91 flows
        if (country_from not in country_B and country_to not in country_A):
            counter +=1
            country_A.append(country_from)
            country_B.append(country_to)
            (country_from, country_to, gravModel(float(kmdist),float(forward_count), float(backward_count), float(lenders_population), float(loans_population)))
    print (counter)
         
def gravModel(distance, forward_count, backward_count, populationA, populationB):
    weight = forward_count + backward_count
    gravity = (populationA * populationB)/(distance*distance)
    if(gravity < 10000000):
        print(gravity)
    plot_gravity.append(gravity)
    weight_flow.append(weight)
    # plot result
    return gravity

print("Using psycopg2…")
myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
doQuery(myConnection)

##Plotting the graph to matplot
x = np.log(plot_gravity)
y = np.log(weight_flow)
weight_flow = np.array(weight_flow)
plot_gravity = np.array(plot_gravity)
plt.plot(x, y, 'ro')
plt.ylabel('F')
plt.xlabel('gravity')

fig, ax = plt.subplots()
fit = np.polyfit(x, y, deg=1)
ax.plot(x, fit[0] * x + fit[1], color='blue')
ax.scatter(x, y)
plt.show()

myConnection.close()
