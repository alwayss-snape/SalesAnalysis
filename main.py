from turtle import color
import matplotlib.pyplot as plt
import pandas as pd
import os
from itertools import combinations, groupby
from collections import Counter
##Merging 12 months of sales data into a single file

"""Read all files from directory"""
files = [file for file in os.listdir("Insert file directory")] 

all_data = pd.DataFrame() #Csv is read as a dataframe in pandas


for file in files:
    df = pd.read_csv("/Users/kshitijchaubey/Desktop/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/" + file)
    all_data = pd.concat([all_data, df])

all_data.to_csv("all_data.csv", index = False)

all_data = pd.read_csv("all_data.csv")
print(all_data.head(100))
#cleaning data
clean_df = all_data[all_data.isna().any(axis=1)]
all_data = all_data.dropna(how='all')

###What was the best month for sales? How much was earned that month?

"""Augment data with additional columns"""
#Add Month Column
all_data['Month'] = all_data['Order Date'].str[0:2]
all_data = all_data[all_data['Order Date'].str[0:2] != 'Or' ]
all_data['Month'] = all_data['Month'].astype('int32')
print(all_data.head())
# Converting columns to their correct type
all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered']) #make int
all_data['Price Each'] = pd.to_numeric(all_data['Price Each'])

#Adding a total sales column
all_data['Sales'] = all_data['Quantity Ordered'] * all_data['Price Each']


Best_Month = all_data.groupby('Month').sum()
print(Best_Month)
months = range(1,13)
plt.bar(months,Best_Month['Sales'], color='Green')
plt.xticks(months)
plt.ylabel("Sales in $USD")
plt.xlabel("Months")
print(plt.show())


#using .apply() method - It is used to apply methods(functions) to columns, lambda x allows to access the contents of the data
def get_city(address):
    return address.split(',')[1]
def get_state(address):
    return address.split(',')[2].split(' ')[1]
all_data['City'] = all_data['Purchase Address'].apply(lambda x: f"{get_city(x)}({get_state(x)})")
print(all_data.tail())

###What City had the highest no. of sales
Best_City = [city for city, df in all_data.groupby('City')]
print(Best_City)
cities = all_data['City'].unique()
plt.bar(cities,Best_City['Sales'])
plt.xticks(cities, rotation = 'vertical', size = 8)
plt.ylabel("Sales in $USD")
plt.xlabel("City Name")
print(plt.show())

###What time should we display advertisements to maximize likelihood of customer's buying product
all_data["Order Date"] = pd.to_datetime(all_data['Order Date'])
all_data['Hour'] = all_data['Order Date'].dt.hour
all_data['Minute'] = all_data['Order Date'].dt.minute

hours = [hour for hour, df in all_data.groupby('Hour')]

plt.plot(hours, all_data.groupby(['Hour']).count())
plt.xticks(hours)
plt.xlabel("Hour")
plt.ylabel("Number of Orders")
plt.grid()
print(plt.show())

###What 2 products are most often sold together?
## Step 1: Finding the duplicate Order ID's to figure out which products were sold together
## Step 2: Creating a new column to have items with same Order IDs in a lie
## Step 3: Dropping duplicates of Grouped Order IDs
## Step 4: Counting the grouped column and getting the top 10 two items that are sold together 

df = all_data[all_data['Order ID'].duplicated(keep=False)] #to mark all duplicate order ids

df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))

df = df[['Order ID','Grouped']].drop_duplicates()

count = Counter()
for row in df['Grouped']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list,2)))
for key, value in count.most_common(10):
    print(key,value)

###What Product Sold the most? Why do you think it sold the most?
product_group = all_data.groupby('Product')
quantity_ordered  = product_group.sum()['Quantity Ordered']

products = [product for product, df in product_group]
plt.bar(products, quantity_ordered)
plt.ylabel('Quantity ordered')
plt.xlabel('Products')

prices = all_data.groupby('Product').mean()['Price Each']
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.bar(products, quantity_ordered, color = 'g')
ax2.plot(products, prices, 'b-')

ax1.set_xlabel('Product name')
ax1.set_ylabel('Quantity Ordered', color = 'g')
ax2.set_ylabel('Price($)', color= 'b')
ax1.set_xticklabels(products, rotation = 'vertical', size = 8)
print(plt.show())

"""This code has various sections for various type of analysis, so comment out the sections that you are not using while running the file"""
