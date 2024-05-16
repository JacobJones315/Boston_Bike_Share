# -*- coding: utf-8 -*-
"""
Created on Thu May  2 22:10:54 2024

@author: Jacob Jones
Date: 5/2/24
"""
import pandas as pd
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import seaborn as sns

# Load your data from specified paths
data_2019 = pd.read_csv(r'C:/Users/jwj12/OneDrive/BANA 6920/bluebikes_tripdata_2019.csv', low_memory=False)
data_2020 = pd.read_csv(r'C:/Users/jwj12/OneDrive/BANA 6920/bluebikes_tripdata_2020.csv', low_memory=False)

# Convert starttime to datetime
data_2020['starttime'] = pd.to_datetime(data_2020['starttime'])

# Extract month, day of week, and hour
data_2020['month'] = data_2020['starttime'].dt.month
data_2020['day_of_week'] = data_2020['starttime'].dt.day_name()
data_2020['hour'] = data_2020['starttime'].dt.hour

most_used_station= data_2020.groupby(['start station id','start station name']).size()


#step 1- fiind the number of trips leaving the station at each hour
# Group by start station, month, day of the week, and hour to get trip counts
hourly_trips = data_2020.groupby(['start station id', 'start station name', 'month', 'day_of_week', 'hour']).size().reset_index(name='trip_count')


# Calculate average and standard deviation of trips per station, month, day of week, and hour
detailed_outflow_stats = hourly_trips.groupby(['start station id', 'start station name', 'month', 'day_of_week', 'hour']).agg(
    average_ouflow_trips=('trip_count', 'mean'),
    std_dev_outflow_trips=('trip_count', 'std')
).reset_index()

# Fill NaN values with 0 for standard deviation in cases where there is only one record for that hour
detailed_outflow_stats['std_dev_outflow_trips'].fillna(0.3*detailed_outflow_stats['average_ouflow_trips'], inplace=True)

# Save or display the result
print(detailed_outflow_stats.head())
print("Columns in the DataFrame:", detailed_outflow_stats.columns)


#step 1- fiind the number of trips coming into the station at each hour
# Group by start station, month, day of the week, and hour to get trip counts
hourly_trips = data_2020.groupby(['end station id', 'end station name', 'month', 'day_of_week', 'hour']).size().reset_index(name='trip_count')


# Calculate average and standard deviation of trips per station, month, day of week, and hour
detailed_inflow_stats = hourly_trips.groupby(['end station id', 'end station name', 'month', 'day_of_week', 'hour']).agg(
    average_inflow_trips=('trip_count', 'mean'),
    std_dev_inflow_trips=('trip_count', 'std')
).reset_index()

# Fill NaN values with 0 for standard deviation in cases where there is only one record for that hour
detailed_inflow_stats['std_dev_inflow_trips'].fillna(.3*detailed_inflow_stats['average_inflow_trips'], inplace=True)

# Save or display the result
print(detailed_inflow_stats.head())
print("Columns in the DataFrame:", detailed_inflow_stats.columns)

# Load your data (this should be replaced with actual data loading)
outflow_data = detailed_outflow_stats
inflow_data = detailed_inflow_stats

# Merge the datasets on common columns
data_merged = pd.merge(outflow_data, inflow_data,  left_on=['start station id', 'start station name', 'month', 'day_of_week', 'hour'],
                        right_on=['end station id', 'end station name', 'month', 'day_of_week', 'hour'],
                        suffixes=('_out', '_in'))

# Calculate net demand
data_merged['net_demand'] = data_merged['average_inflow_trips'] - data_merged['average_ouflow_trips']

# Calculate the standard deviation of net demand
data_merged['std_dev_net_demand'] = np.sqrt(data_merged['std_dev_outflow_trips']**2 + data_merged['std_dev_inflow_trips']**2)

# Define the service level and find the corresponding z-score
service_level = 0.95
z_score = norm.ppf(service_level)

# Calculate the optimal number of bikes to stock at each station per hour
data_merged['optimal_bikes_stock'] = data_merged['net_demand'] + (data_merged['std_dev_net_demand'] * z_score)

# Save or display the result
print(data_merged.head())
data_merged.to_csv(r'C:\Users\jwj12\OneDrive\BANA 6920\stock levels.csv', index=False)


print("Columns in the DataFrame:", data_merged.columns)


def plot_bike_stock_for_month(station_id, month):
    # Define days of the week
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Set up the plotting environment
    plt.figure(figsize=(18, 12))  # Adjust the size as needed
    
    for i, day in enumerate(days_of_week, 1):
        # Filter the data for the selected station ID, month, and day of the week
        filtered_data = data_merged[(data_merged['start station id'] == station_id) & 
                                    (data_merged['month'] == month) & 
                                    (data_merged['day_of_week'] == day)]
        print(i,day)
        # Sort values by hour to ensure the line plot makes sense
        filtered_data = filtered_data.sort_values('hour')
        
        # Plot configuration for each subplot
        plt.subplot(3, 3, i)  # Adjust the grid size if needed, 3x3 for 7 plots provides an extra space
        sns.lineplot(x='hour', y='optimal_bikes_stock', data=filtered_data, marker='o')
        
        # Adding title and labels
        plt.title(f'Station {station_id} - {day}')
        plt.xlabel('Hour of the Day')
        plt.ylabel('Optimal Bikes Stock')
        plt.grid(True)
    
    plt.tight_layout()  # Adjust layout to prevent overlap
    plt.show()

# Call the function with a specific station ID and month
plot_bike_stock_for_month(68, 2) 
