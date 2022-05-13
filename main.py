from turtle import color
import matplotlib.pyplot as plt
import pandas as pd
import os
##Merging 12 months of sales data into a single file
df = pd.read_csv("/Users/kshitijchaubey/Desktop/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/Sales_April_2019.csv")


"""Read all files from directory"""
files = [file for file in os.listdir("/Users/kshitijchaubey/Desktop/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data")] 

all_data = pd.DataFrame() #Csv is read as a dataframe in pandas


for file in files:
    df = pd.read_csv("/Users/kshitijchaubey/Desktop/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/" + file)
    all_data = pd.concat([all_data, df])

all_data.to_csv("all_data.csv", index = False)

all_data = pd.read_csv("all_data.csv")
# print(all_data.head(100))
#cleaning data
clean_df = all_data[all_data.isna().any(axis=1)]
all_data = all_data.dropna(how='all')

#What was the best month for sales? How much was earned that month?

"""Augment data with additional columns"""
#Add Month Column
all_data['Month'] = all_data['Order Date'].str[0:2]
all_data = all_data[all_data['Order Date'].str[0:2] != 'Or' ]
all_data['Month'] = all_data['Month'].astype('int32')
# print(all_data.head())
### Converting columns to their correct type
all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered']) #make int
all_data['Price Each'] = pd.to_numeric(all_data['Price Each'])

#Adding a total sales column
all_data['Sales'] = all_data['Quantity Ordered'] * all_data['Price Each']


# Best_Month = all_data.groupby('Month').sum()
# # print(Best_Month)
# months = range(1,13)
# plt.bar(months,Best_Month['Sales'], color='Green')
# plt.xticks(months)
# plt.ylabel("Sales in $USD")
# plt.xlabel("Months")
# print(plt.show())


#using .apply() method - It is used to apply methods(functions) to columns, lambda x allows to access the contents of the data
def get_city(address):
    return address.split(',')[1]
def get_state(address):
    return address.split(',')[2].split(' ')[1]
all_data['City'] = all_data['Purchase Address'].apply(lambda x: f"{get_city(x)}({get_state(x)})")
# print(all_data.tail())

###What City had the highest no. of sales
Best_City = [city for city, df in all_data.groupby('City')]
# print(Best_City)
# cities = all_data['City'].unique()
# plt.bar(cities,Best_City['Sales'])
# plt.xticks(cities, rotation = 'vertical', size = 8)
# plt.ylabel("Sales in $USD")
# plt.xlabel("City Name")
# print(plt.show())

#What time should we display advertisements to maximize likelihood of customer's buying product
all_data["Order Date"] = pd.to_datetime(all_data['Order Date'])
all_data['Hour'] = all_data['Order Date'].dt.hour
all_data['Minute'] = all_data['Order Date'].dt.minute

hours = [hour for hour, df in all_data.groupby('Hour')]

print(plt.plot(hours, all_data.groupby(['Hour']).count()))

