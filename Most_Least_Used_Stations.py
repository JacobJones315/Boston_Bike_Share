"""
Created on Thu May  2 07:11:13 2024

@author: Jacob Jones
Date: 5/2/24
"""

import pandas as pd
import matplotlib.pyplot as plt


bikes2019 = pd.read_csv(r'C:/Users/jwj12/OneDrive/BANA 6920/bluebikes_tripdata_2019.csv')
bikes2019['starttime'] = pd.to_datetime(bikes2019['starttime'])
bikes2019['stoptime'] = pd.to_datetime(bikes2019['stoptime'])
bikes2019['day_of_year'] = bikes2019['starttime'].dt.dayofyear
bikes2019['hour']= bikes2019['starttime'].dt.hour
bikes2019['day_of_week']= bikes2019['starttime'].dt.dayofweek

bikes2019.head()
bikes2019.info()

bikes2019['tripduration_min'] = (bikes2019['tripduration'] / 60).round(2)
bikes2019.drop(columns=['tripduration'], inplace = True)


#importing bikes 2020, need to convert postal code to dtype string due to input errors 
bikes2020 = pd.read_csv(r'C:/Users/jwj12/OneDrive/BANA 6920/bluebikes_tripdata_2020.csv', dtype={'postal code': str})
bikes2020['starttime'] = pd.to_datetime(bikes2020['starttime'])
bikes2020['stoptime'] = pd.to_datetime(bikes2020['stoptime'])
bikes2020['day_of_year'] = bikes2020['starttime'].dt.dayofyear
bikes2020['hour']= bikes2020['starttime'].dt.hour
bikes2020['day_of_week']= bikes2020['starttime'].dt.dayofweek

bikes2020.info()
bikes2020.head()

bikes2020['tripduration_min'] = (bikes2020['tripduration'] / 60).round(2)
bikes2020.drop(columns=['tripduration'], inplace = True)


# Merge the two DataFrames
bikes_data = pd.concat([bikes2019, bikes2020], ignore_index=True)


# Finding the most frequently used start stations in 2019
frequent_start_stations_2019 = bikes2019.groupby('start station id', as_index=False).size().sort_values(by='size', ascending=False).head(10)
frequent_start_stations_2019 = frequent_start_stations_2019.reset_index(drop=True)
frequent_start_stations_2019.index += 1
print("Most frequently used start stations:")
print(frequent_start_stations_2019)


# Group by hour and start station and count occurrences
stations_by_hour = bikes_data.groupby(['hour', 'start station id', 'tripduration_min']).size().reset_index(name='count')



# extracting Station 60 count by hour
Top_stations = bikes_data.loc[(bikes_data['start station id'] == 60) | (bikes_data['start station id'] == 67) | (bikes_data['start station id'] == 68)]



# Counting outputs per station per hour
outputs_by_hour = Top_stations.groupby(['hour', 'start station id']).size().reset_index(name='output_count')

# Counting inputs per station per hour
inputs_by_hour = Top_stations.groupby(['hour', 'end station id']).size().reset_index(name='input_count')



# extracting Station 67 count by hour
station_67_outflow = stations_by_hour.loc[stations_by_hour['start station id'] == 67]

# extracting Station 68 count by hour
station_68_outflow = stations_by_hour.loc[stations_by_hour['start station id'] == 68]


# Group by hour and start station and count occurrences
stations_by_hour2 = bikes_data.groupby(['hour', 'end station id']).size().reset_index(name='count')
stations_by_hour2.index += 1

# extracting Station 60 count by hour
station_60_inflow = stations_by_hour2.loc[stations_by_hour2['end station id'] == 60]

# extracting Station 67 count by hour
station_67_inflow = stations_by_hour2.loc[stations_by_hour2['end station id'] == 67]

# extracting Station 68 count by hour
station_68_inflow = stations_by_hour2.loc[stations_by_hour2['end station id'] == 68]


# Find the most frequently used end stations in 2019
frequent_end_stations_2019 = bikes2019['end station id'].value_counts().head(10)
print("\nMost frequently used end stations:")
print(frequent_end_stations_2019)


frequent_start_stations_20191 = bikes2019['start station id'].value_counts().head(10)
print("\nMost frequently used end stations:")
print(frequent_start_stations_20191)



# Finding the most frequently used start stations in 2020
frequent_start_stations_2020 = bikes2020['start station id'].value_counts().head(10)
print("Most frequently used start stations:")
print(frequent_start_stations_2020)

# Find the most frequently used end stations in 2020
frequent_end_stations_2020 = bikes2020['end station id'].value_counts().head(10)
print("\nMost frequently used end stations:")
print(frequent_end_stations_2020)



#Plotting
plt.figure(figsize=(15, 10))

# Subplot 1: Most frequently used start stations in 2019
plt.subplot(2, 2, 1)  # 2 rows, 2 columns, 1st subplot
frequent_start_stations_20191.plot(kind='bar', color='teal')
plt.title('Most Frequently Used Start Stations in 2019')
plt.xlabel('Station ID')
plt.ylabel('Frequency')
plt.xticks(rotation=45)

# Subplot 2: Most frequently used end stations in 2019
plt.subplot(2, 2, 2)  # 2 rows, 2 columns, 2nd subplot
frequent_end_stations_2019.plot(kind='bar', color='blue')
plt.title('Most Frequently Used End Stations in 2019')
plt.xlabel('Station ID')
plt.ylabel('Frequency')
plt.xticks(rotation=45)

# Subplot 3: Most frequently used start stations in 2020
plt.subplot(2, 2, 3)  # 2 rows, 2 columns, 3rd subplot
frequent_start_stations_2020.plot(kind='bar', color='purple')
plt.title('Most Frequently Used Start Stations in 2020')
plt.xlabel('Station ID')
plt.ylabel('Frequency')
plt.xticks(rotation=45)

# Subplot 4: Most frequently used end stations in 2020
plt.subplot(2, 2, 4)  # 2 rows, 2 columns, 4th subplot
frequent_end_stations_2020.plot(kind='bar', color='magenta')
plt.title('Most Frequently Used End Stations in 2020')
plt.xlabel('Station ID')
plt.ylabel('Frequency')
plt.xticks(rotation=45)

plt.tight_layout()  # Adjust the layout to make sure there's no overlap
plt.show()



# 2019 Least frequently used end stations
least_used_start_stations_2019 = bikes2019['start station id'].value_counts().tail(10)
print("Least frequently used start stations in 2019:")
print(least_used_start_stations_2019)


# 2019 Least frequently used end stations
least_used_end_stations_2019 = bikes2019['end station id'].value_counts().tail(10)
print("\nLeast frequently used end stations:")
print(least_used_end_stations_2019)


# 2020 Least frequently used start stations
least_used_start_stations_2020 = bikes2020['start station id'].value_counts().tail(10)
print("Least frequently used start stations:")
print(least_used_start_stations_2020)

# 2020 Least frequently used end stations
least_used_end_stations_2020 = bikes2020['end station id'].value_counts().tail(10)
print("\nLeast frequently used end stations:")
print(least_used_end_stations_2020)

#Plotting 


# Define the figure and axes for a 2x2 grid of plots
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15, 10))

# Plot for least frequently used start stations in 2019
least_used_start_stations_2019.plot(kind='bar', color='red', ax=axes[0, 0])  # top left
axes[0, 0].set_title('Least Frequently Used Start Stations 2019')
axes[0, 0].set_xlabel('Station ID')
axes[0, 0].set_ylabel('Frequency')
axes[0, 0].tick_params(axis='x', rotation=45)

# Plot for least frequently used end stations in 2019
least_used_end_stations_2019.plot(kind='bar', color='maroon', ax=axes[0, 1])  # top right
axes[0, 1].set_title('Least Frequently Used End Stations 2019')
axes[0, 1].set_xlabel('Station ID')
axes[0, 1].set_ylabel('Frequency')
axes[0, 1].tick_params(axis='x', rotation=45)

# Plot for least frequently used start stations in 2020
least_used_start_stations_2020.plot(kind='bar', color='red', ax=axes[1, 0])  # bottom left
axes[1, 0].set_title('Least Frequently Used Start Stations 2020')
axes[1, 0].set_xlabel('Station ID')
axes[1, 0].set_ylabel('Frequency')
axes[1, 0].tick_params(axis='x', rotation=45)

# Plot for least frequently used end stations in 2020
least_used_end_stations_2020.plot(kind='bar', color='maroon', ax=axes[1, 1])  # bottom right
axes[1, 1].set_title('Least Frequently Used End Stations 2020')
axes[1, 1].set_xlabel('Station ID')
axes[1, 1].set_ylabel('Frequency')
axes[1, 1].tick_params(axis='x', rotation=45)

# Adjust layout to prevent overlap
plt.tight_layout()
plt.show()
