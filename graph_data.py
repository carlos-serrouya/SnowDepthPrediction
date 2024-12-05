import numpy as np
import matplotlib.pyplot as plt

#todo add name of location to data
# todo add more data
# todo imporove model
# todo verify data

# data format: 
# [longitude, latitude, avg_summer_max, avg_summer_low, total_summer_rain, average_previous_snowfall, lanina_data, elnino_data, laninaintensity_data, elninointensity_data, carbon_data, elevation, season, yearly_snow]
# Constants for var locations:
LONGITUDE = 0
LATITUDE = 1
AVG_SUMMER_MAX = 2
AVG_SUMMER_LOW = 3
TOTAL_SUMMER_RAIN = 4
AVERAGE_PREVIOUS_SNOWFALL = 5
LANINA_DATA = 6
ELNINO_DATA = 7
LANINAINTENSITY_DATA = 8
ELNINOINTENSITY_DATA = 9
CARBON_DATA = 10
ELEVATION = 11
SEASON = 12
YEARLY_SNOW = 13

#bar chart with average per el nino and la nina and their intensity

#load data
data = np.load("processed_data.npy", allow_pickle=True)

#initialize variables
elNinoIntensity1 = []
elNinoIntensity2 = []
elNinoIntensity3 = []
elNinoIntensity4 = []
neither = []
laNinaIntensity1 = []
laNinaIntensity2 = []
laNinaIntensity3 = []
laNinaIntensity4 = []

#iterate through data
for i in range(len(data)):
    #check if el nino
    if data[i][ELNINO_DATA] == 1:
        #check intensity
        if data[i][ELNINOINTENSITY_DATA] == 1:
            elNinoIntensity1.append(data[i][YEARLY_SNOW])
        elif data[i][ELNINOINTENSITY_DATA] == 2:
            elNinoIntensity2.append(data[i][YEARLY_SNOW])
        elif data[i][ELNINOINTENSITY_DATA] == 3:
            elNinoIntensity3.append(data[i][YEARLY_SNOW])
        elif data[i][ELNINOINTENSITY_DATA] == 4:
            elNinoIntensity4.append(data[i][YEARLY_SNOW])

    elif data[i][LANINA_DATA] == 1:
        #check intensity
        if data[i][LANINAINTENSITY_DATA] == 1:
            laNinaIntensity1.append(data[i][YEARLY_SNOW])
        elif data[i][LANINAINTENSITY_DATA] == 2:
            laNinaIntensity2.append(data[i][YEARLY_SNOW])
        elif data[i][LANINAINTENSITY_DATA] == 3:
            laNinaIntensity3.append(data[i][YEARLY_SNOW])
        elif data[i][LANINAINTENSITY_DATA] == 4:
            laNinaIntensity4.append(data[i][YEARLY_SNOW])
        
    #neither
    else:
        neither.append(data[i][YEARLY_SNOW])

print(len(elNinoIntensity1))
print(len(laNinaIntensity1))
print(len(neither))
print(len(elNinoIntensity2))
print(len(laNinaIntensity2))
print(len(elNinoIntensity3))
print(len(laNinaIntensity3))
print(len(elNinoIntensity4))
print(len(laNinaIntensity4))

all_elNino = elNinoIntensity1 + elNinoIntensity2 + elNinoIntensity3 + elNinoIntensity4
all_laNina = laNinaIntensity1 + laNinaIntensity2 + laNinaIntensity3 + laNinaIntensity4

# todo add anova test

plt.bar("El Nino", np.mean(all_elNino))
plt.bar("Neither", np.mean(neither))
plt.bar("La Nina", np.mean(all_laNina))

# #plot data
# plt.bar("El Nino Intensity 4", np.mean(elNinoIntensity4))
# plt.bar("El Nino Intensity 3", np.mean(elNinoIntensity3))
# plt.bar("El Nino Intensity 2", np.mean(elNinoIntensity2))
# plt.bar("El Nino Intensity 1", np.mean(elNinoIntensity1))
# plt.bar("Neither", np.mean(neither))
# plt.bar("La Nina Intensity 1", np.mean(laNinaIntensity1))
# plt.bar("La Nina Intensity 2", np.mean(laNinaIntensity2))
# plt.bar("La Nina Intensity 3", np.mean(laNinaIntensity3))
# plt.bar("La Nina Intensity 4", np.mean(laNinaIntensity4))


#show plot
plt.show()



#todo regression
elevation = []
snow = []

for i in range(len(data)):
    elevation.append(data[i][ELEVATION])
    snow.append(data[i][YEARLY_SNOW])

#plot data in line graph
plt.plot(elevation, snow)

#show plot
plt.show()

#todo regression on normalized per deployment data
carbon = []
snow = []

for i in range(len(data)):
    carbon.append(data[i][CARBON_DATA])
    snow.append(data[i][YEARLY_SNOW])

#plot data in line graph
plt.plot(carbon, snow)

#show plot
plt.show()


#just do this for biggest deployment
summerRain = []
summerMax = []
snow = []

for i in range(len(data)):
    summerRain.append(data[i][TOTAL_SUMMER_RAIN])
    summerMax.append(data[i][AVG_SUMMER_MAX])
    snow.append(data[i][YEARLY_SNOW])

#plot data in scatter plot
plt.scatter(summerRain, summerMax, c=snow)

#show plot
plt.show()