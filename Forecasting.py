
"""
Created on Thu Apr  4 18:51:05 2024

@author: Jacob Jones
Date: 5/1/24
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
# double and triple exponential smoothing
from statsmodels.tsa.holtwinters import ExponentialSmoothing


bikes2019 = pd.read_csv('C:/Users/jwj12/OneDrive/BANA 6920/bluebikes_tripdata_2019.csv')
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
bikes2020 = pd.read_csv('C:/Users/jwj12/OneDrive/BANA 6920/bluebikes_tripdata_2020.csv', dtype={'postal code': str})
bikes2020['starttime'] = pd.to_datetime(bikes2020['starttime'])
bikes2020['stoptime'] = pd.to_datetime(bikes2020['stoptime'])
bikes2020['day_of_year'] = bikes2020['starttime'].dt.dayofyear
bikes2020['hour']= bikes2020['starttime'].dt.hour
bikes2020['day_of_week']= bikes2020['starttime'].dt.dayofweek

bikes2020.info()
bikes2020.head()

bikes2020['tripduration_min'] = (bikes2020['tripduration'] / 60).round(2)
bikes2020.drop(columns=['tripduration'], inplace = True)


bikes1920= pd.concat([bikes2019,bikes2020], sort=False, axis=0, ignore_index=True)
bikes1920.head() 
bikes1920.info()



## found a csv of all Zip codes in the state of Massachusets, our dataset has zipcodes throughout the entire state and input errors
MAzipcodes = pd.read_csv('C:/Users/jwj12/OneDrive/BANA 6920/Zips.csv', dtype={'zip': str})
MAzipcodes.head()
MAzipcodes.info()


Customers2019 = bikes2019.loc[bikes2019['usertype'] == 'Customer']
Customer_sales2019 = Customers2019[['starttime', 'usertype']].copy()
Customer_sales2019.rename(columns={'usertype':'Customer_Sales'}, inplace=True)
Customer_sales_by_day_2019 = Customer_sales2019.groupby(pd.Grouper(key='starttime', freq='D', origin='start')).count().reset_index()

Subscribers2019 = bikes2019.loc[bikes2019['usertype'] == 'Subscriber']
Subscriber_sales2019 = Subscribers2019[['starttime', 'usertype']].copy()
Subscriber_sales2019.rename(columns={'usertype':'Subscriber_Sales'}, inplace=True)
Subscriber_sales_by_day_2019 = Subscriber_sales2019.groupby(pd.Grouper(key='starttime', freq='D', origin='start')).count().reset_index()



#filtering out subscribers
Customers2020 = bikes2020.loc[bikes2020['usertype'] == 'Customer']
nan_count_per_column1 = Customers2020.isna().sum()
summary_stats1 = Customers2020.describe()


#all in one step ignore, havent filtered out postal code errors
Customer_Postalcodes1 = (bikes2020.loc[bikes2020['usertype'] == 'Customer'].groupby('postal code')
                         .count().reset_index().rename(columns={'usertype':'Customers'})[['postal code', 'Customers']])


Customer_Postalcodes = Customers2020.groupby('postal code')['usertype'].count().reset_index()
Customer_Postalcodes.info()


#filtering out customers
Subscribers = bikes2020.loc[bikes2020['usertype'] == 'Subscriber']
nan_count_per_column2 = Subscribers.isna().sum()
summary_stats2 = Subscribers.describe()


#finding the # of subscribers per postal code
Subscriber_Postalcodes = Subscribers.groupby('postal code')['usertype'].count().reset_index()
Subscriber_Postalcodes.info()


####################### Customer/Subscriber Weekly Sales use for forecasting
Customer_sales2020 = Customers2020[['starttime', 'usertype']].copy()
Customer_sales2020.rename(columns={'usertype':'Customer_Sales'}, inplace=True)


Customer_sales_by_Week_2020 = Customer_sales2020.groupby(pd.Grouper(key='starttime', freq='1W', origin='start')).count().reset_index()


Customer_sales_by_Week_2019 = Customer_sales2019.groupby(pd.Grouper(key='starttime', freq='1W', origin='start')).count().reset_index()
Subscriber_sales_by_Week_2019 = Subscriber_sales2019.groupby(pd.Grouper(key='starttime', freq='1W', origin='start')).count().reset_index()



Subscriber_sales2020= Subscribers[['starttime', 'usertype']].copy()
Subscriber_sales2020.rename(columns={'usertype':'Subscriber_Sales'}, inplace=True)


Subscriber_sales_by_Week_2020 = Subscriber_sales2020.groupby(pd.Grouper(key='starttime', freq='1W', origin='start')).count().reset_index()


Forecast_Subscriber_sales_by_Week_2020 = Subscriber_sales2020.groupby(pd.Grouper(key='starttime', freq='1W', origin='start')).count().reset_index()
Forecast_Subscriber_sales_by_Week_2019 = Subscriber_sales2019.groupby(pd.Grouper(key='starttime', freq='1W', origin='start')).count().reset_index()

Subscriber_weekly_sales_1920 = pd.concat([Forecast_Subscriber_sales_by_Week_2019,Forecast_Subscriber_sales_by_Week_2020], sort=False, axis=0, ignore_index=True)
Subscriber_weekly_sales_1920 = Subscriber_weekly_sales_1920.drop(range(48,52)).reset_index(drop=True)
Subscriber_weekly_sales_1920 = Subscriber_weekly_sales_1920.drop(97).reset_index(drop=True)
Subscriber_weekly_sales_1920 = Subscriber_weekly_sales_1920.drop(48).reset_index(drop=True)

Subscriber_weekly_sales_1920.set_index('starttime', inplace=True)

Subscriber_weekly_sales_1920['SWS_ADD'] = ExponentialSmoothing(Subscriber_weekly_sales_1920['Subscriber_Sales'],trend='add',seasonal='add',seasonal_periods=12).fit().fittedvalues
Subscriber_weekly_sales_1920['SWS_MUL'] = ExponentialSmoothing(Subscriber_weekly_sales_1920['Subscriber_Sales'],trend='mul',seasonal='mul',seasonal_periods=12).fit().fittedvalues

fig6, ax6 =plt.subplots(dpi = 100, figsize = (30,10))
Subscriber_weekly_sales_1920[['Subscriber_Sales','SWS_ADD','SWS_MUL']].plot(ax=ax6)
ax6.set_xlabel('Date')
ax6.set_ylabel('Sales')
ax6.set_title('2019-2020 Subscriber Holt Winters Triple Exponential Smoothing: Additive and Multiplicative Seasonality')
# Add legend with appropriate labels
ax6.legend(['Actual Sales', 'Additive Seasonality', 'Multiplicative Seasonality'], loc='upper left', fontsize='large')


Subscriber_weekly_sales_1920['ADD_APE'] = np.abs((Subscriber_weekly_sales_1920['Subscriber_Sales'] - Subscriber_weekly_sales_1920['SWS_ADD']) / Subscriber_weekly_sales_1920['Subscriber_Sales']) * 100
ADD_Monthly_MAPE_sub = Subscriber_weekly_sales_1920['ADD_APE'].mean()
Subscriber_weekly_sales_1920['MUL_APE'] = np.abs((Subscriber_weekly_sales_1920['Subscriber_Sales'] - Subscriber_weekly_sales_1920['SWS_MUL']) / Subscriber_weekly_sales_1920['Subscriber_Sales']) * 100
MUL_Monthly_MAPE_sub = Subscriber_weekly_sales_1920['MUL_APE'].mean()
# transform=ax6.transAxes means coordinates are relative to the axes, not the data
#The text displayed is formatted using an f-string, where {ADD_Monthly_MAPE_sub:.2f}% inserts the value of ADD_Monthly_MAPE_sub rounded to two decimal places followed by a percentage sign.
ax6.text(0.05, 0.85, f'Additive Seasonality MAPE: {ADD_Monthly_MAPE_sub:.2f}%', transform=ax6.transAxes, fontsize=12, verticalalignment='top')
ax6.text(0.05, 0.75, f'Multiplicative Seasonality MAPE: {MUL_Monthly_MAPE_sub:.2f}%', transform=ax6.transAxes, fontsize=12, verticalalignment='top')






########################################################################################

Forecast_Customer_sales_by_Week_2020 = Customer_sales2020.groupby(pd.Grouper(key='starttime', freq='1W', origin='start')).count().reset_index()
Forecast_Customer_sales_by_Week_2019 = Customer_sales2019.groupby(pd.Grouper(key='starttime', freq='1W', origin='start')).count().reset_index()

Customer_weekly_sales_1920 = pd.concat([Forecast_Customer_sales_by_Week_2019,Forecast_Customer_sales_by_Week_2020], sort=False, axis=0, ignore_index=True)
Customer_weekly_sales_1920 = Customer_weekly_sales_1920.drop(range(48,52)).reset_index(drop=True)
Customer_weekly_sales_1920 = Customer_weekly_sales_1920.drop(97).reset_index(drop=True)
Customer_weekly_sales_1920 = Customer_weekly_sales_1920.drop(48).reset_index(drop=True)

Customer_weekly_sales_1920.set_index('starttime', inplace=True)


Customer_weekly_sales_1920['CWS_ADD'] = ExponentialSmoothing(Customer_weekly_sales_1920['Customer_Sales'],trend='add',seasonal='add',seasonal_periods=12).fit().fittedvalues
Customer_weekly_sales_1920['CWS_MUL'] = ExponentialSmoothing(Customer_weekly_sales_1920['Customer_Sales'],trend='mul',seasonal='mul',seasonal_periods=12).fit().fittedvalues



fig7, ax7 =plt.subplots(dpi = 100, figsize = (30,10))
Customer_weekly_sales_1920[['Customer_Sales','CWS_ADD','CWS_MUL']].plot(ax=ax7)
ax7.set_xlabel('Date')
ax7.set_ylabel('Sales')
ax7.set_title('2019-2020 Customer Holt Winters Triple Exponential Smoothing: Additive and Multiplicative Seasonality')
# Add legend with appropriate labels
ax7.legend(['Actual Sales', 'Additive Seasonality', 'Multiplicative Seasonality'], loc='upper left', fontsize='large')

Customer_weekly_sales_1920['ADD_APE'] = np.abs((Customer_weekly_sales_1920['Customer_Sales'] - Customer_weekly_sales_1920['CWS_ADD']) / Customer_weekly_sales_1920['Customer_Sales']) * 100
ADD_Monthly_MAPE_cust = Customer_weekly_sales_1920['ADD_APE'].mean()
Customer_weekly_sales_1920['MUL_APE'] = np.abs((Customer_weekly_sales_1920['Customer_Sales'] - Customer_weekly_sales_1920['CWS_MUL']) / Customer_weekly_sales_1920['Customer_Sales']) * 100
MUL_Monthly_MAPE_cust = Customer_weekly_sales_1920['MUL_APE'].mean()
ax7.text(0.05, 0.85, f'Additive Seasonality MAPE: {ADD_Monthly_MAPE_cust:.2f}%', transform=ax7.transAxes, fontsize=12, verticalalignment='top')
ax7.text(0.05, 0.75, f'Multiplicative Seasonality MAPE: {MUL_Monthly_MAPE_cust:.2f}%', transform=ax7.transAxes, fontsize=12, verticalalignment='top')



customer1920 = Customer_weekly_sales_1920.copy()




model = ExponentialSmoothing(customer1920['Customer_Sales'],trend='mul',seasonal='mul',seasonal_periods=12).fit()


# Forecast future values with datetime index corresponding to future dates
future_index = pd.date_range(start=customer1920.index[-1], periods=12, freq='W')  # Assuming weekly frequency
Customer_future_predictions = model.forecast(12)



# Create DataFrame with future_index as index and future_predictions as column
Customer_future_df = pd.DataFrame({'Date': future_index, 'Forecasted_Sales': Customer_future_predictions})

Customer_future_df.set_index('Date', inplace=True)


fig11, ax11 =plt.subplots(dpi = 100, figsize = (30,10))

customer1920['Customer_Sales'].plot(ax=ax11, legend=True, label='Historical Data')
Customer_future_df['Forecasted_Sales'].plot(ax=ax11, legend=True, label='Forecasted Values')

ax11.set_title('Customer Historical Bike Rentals and Future Forecasted Values')
ax11.set_xlabel('Date')
ax11.set_ylabel('Bike Rentals')



##########

subscriber1920 = Subscriber_weekly_sales_1920.copy()



model2 = ExponentialSmoothing(subscriber1920['Subscriber_Sales'],trend='mul',seasonal='mul',seasonal_periods=12).fit()


Subscriber_future_index = pd.date_range(start=subscriber1920.index[-1], periods=12, freq='W')  # Assuming weekly frequency

Subscriber_future_predictions = model2.forecast(12)



# Create DataFrame with future_index as index and future_predictions as column
Subscriber_future_df = pd.DataFrame({'Date': Subscriber_future_index, 'Forecasted_Sales': Subscriber_future_predictions})

Subscriber_future_df.set_index('Date', inplace=True)


fig12, ax12 =plt.subplots(dpi = 100, figsize = (30,10))

subscriber1920['Subscriber_Sales'].plot(ax=ax12, legend=True, label='Historical Data')
Subscriber_future_df['Forecasted_Sales'].plot(ax=ax12, legend=True, label='Forecasted Values')

ax12.set_title('Subscriber Historical Bike Rentals and Future Forecasted Values')
ax12.set_xlabel('Date')
ax12.set_ylabel('Bike Rentals')


#################################################################


import numpy as np 
from sklearn import linear_model



#Importing_csv_files to do regression

##Customers
Customer_Regression_csv = pd.read_csv('C:/Users/jwj12/OneDrive/BANA 6920/Customer_Sales_Regression.csv')
Subscriber_Regression_csv = pd.read_csv('C:/Users/jwj12/OneDrive/BANA 6920/Subscriber_Sales_Regression.csv')


Customer_reg = linear_model.LinearRegression()
Customer_reg.fit(Customer_Regression_csv[['Temp','Precipitation']], Customer_Regression_csv['Customer_Sales'])


# define and estimate model

# obtain fit statistics
Customer_coeffs = Customer_reg.coef_
Customer_intercept = Customer_reg.intercept_
Customer_r_squared = Customer_reg.score(Customer_Regression_csv[['Temp','Precipitation']], Customer_Regression_csv['Customer_Sales'])

Customer_Regression_csv.drop(columns=Customer_Regression_csv.columns[4:13], inplace=True)
Customer_Regression_csv['Forecast']= Customer_intercept + Customer_coeffs[0] * Customer_Regression_csv['Temp'] + Customer_coeffs[1] * Customer_Regression_csv['Precipitation']



##Subscribers

Subscriber_reg = linear_model.LinearRegression()
Subscriber_reg.fit(Subscriber_Regression_csv[['Temp','Precipitation']], Subscriber_Regression_csv['Subscriber_Sales'])

# define and estimate model

# obtain fit statistics
Subscriber_coeffs = Subscriber_reg.coef_
Subscriber_intercept = Subscriber_reg.intercept_
Subscriber_r_squared = Subscriber_reg.score(Subscriber_Regression_csv[['Temp','Precipitation']], Subscriber_Regression_csv['Subscriber_Sales'])

Subscriber_Regression_csv.drop(columns=Subscriber_Regression_csv.columns[4:18], inplace=True)
Subscriber_Regression_csv['Forecast']= Subscriber_intercept + Subscriber_coeffs[0] * Subscriber_Regression_csv['Temp'] + Subscriber_coeffs[1] * Subscriber_Regression_csv['Precipitation']


#Customer_sales_by_Week_2020 = Customer_sales2020.groupby(pd.Grouper(key='starttime', freq='1W', origin='start')).count().reset_index()

fig3, ax3 =plt.subplots(dpi = 100, figsize = (30,10))
ax3.plot(Customer_sales_by_Week_2020['starttime'], Customer_sales_by_Week_2020['Customer_Sales'], marker='o', linestyle='-')
ax3.set_xlabel('Weeks')
ax3.set_ylabel('Sales')
ax3.set_title('Customer Weekly Sales 2020')
plt.grid(True)

#Subscriber_sales_by_Week_2020 = Subscriber_sales2020.groupby(pd.Grouper(key='starttime', freq='1W', origin='start')).count().reset_index()

fig4,ax4 = plt.subplots(dpi = 100, figsize = (30,10))
ax4.plot(Subscriber_sales_by_Week_2020['starttime'], Subscriber_sales_by_Week_2020['Subscriber_Sales'], marker='o', linestyle='-')
ax4.set_xlabel('Weeks')
ax4.set_ylabel('Sales')
ax4.set_title('Subscriber Weekly Sales 2020')
plt.grid(True)


#Subscriber_sales_by_Week_2019 = Subscriber_sales2019.groupby(pd.Grouper(key='starttime', freq='1W', origin='start')).count().reset_index()

fig9,ax9 = plt.subplots(dpi = 100, figsize = (30,10))
ax9.plot(Subscriber_sales_by_Week_2019['starttime'], Subscriber_sales_by_Week_2019['Subscriber_Sales'], marker='o', linestyle='-')
ax9.set_xlabel('Weeks')
ax9.set_ylabel('Sales')
ax9.set_title('Subscriber Weekly Sales 2019')
plt.grid(True)

#Customer_sales_by_Week_2019 = Customer_sales2019.groupby(pd.Grouper(key='starttime', freq='1W', origin='start')).count().reset_index()

fig10,ax10 = plt.subplots(dpi = 100, figsize = (30,10))
ax10.plot(Customer_sales_by_Week_2019['starttime'], Customer_sales_by_Week_2019['Customer_Sales'], marker='o', linestyle='-')
ax10.set_xlabel('Weeks')
ax10.set_ylabel('Sales')
ax10.set_title('Customer Weekly Sales 2019')
plt.grid(True)


# performing a left join to only include the zipcodes in the state of MA 
Customer_Zips = MAzipcodes.merge(Customer_Postalcodes, left_on='zip', right_on='postal code', how='left')
Customer_Zips.head() 
Customer_Zips.dropna(inplace=True)

Subscriber_Zips = MAzipcodes.merge(Subscriber_Postalcodes, left_on='zip', right_on='postal code', how='left')
Subscriber_Zips.head() 
Subscriber_Zips.dropna(inplace=True)

CZ=Customer_Zips[['zip','usertype']].copy()
CZ.rename(columns={'usertype':'Customers'}, inplace=True)

subs=Subscriber_Zips[['zip','usertype']].copy()
subs.rename(columns={'usertype':'Subscribers'},inplace = True)

customer_subscriber_ratio = CZ.merge(subs, how='inner', on='zip')
customer_subscriber_ratio['Customer/Subscriber Ratio'] = (customer_subscriber_ratio['Customers']/customer_subscriber_ratio['Subscribers']) * 100

#exporting to excell to create graphic for customer/subscribers ratio, changing to float so i can adjust in excel
customer_subscriber_ratio.to_csv(r'C:\Users\jwj12\OneDrive\BANA 6920\csr.csv',float_format='%.2f', index=False)


#exporting to excell to create a heat map of nonsubscribers per zipcode
Customer_Zips.to_csv(r'C:\Users\jwj12\OneDrive\BANA 6920\Bike_zips.csv', index=False)

#exporting to excell to create a heat map of subscribers per zipcode
Subscriber_Zips.to_csv(r'C:\Users\jwj12\OneDrive\BANA 6920\Subscriber_zips.csv', index=False)



# creating an interactive map that shows each start station usage per minute
Map = bikes1920.groupby(['start station name', 'start station latitude', 'start station longitude'])['tripduration_min'].sum().reset_index()

# most used routes
most_used_route =bikes1920.groupby(['start station name','start station latitude',
    'start station longitude', 'end station name', 'end station latitude',
        'end station longitude'])['starttime'].count().reset_index()



import requests

url = "https://route-and-directions.p.rapidapi.com/v1/routing"

querystring = {"waypoints":"42.3596,-71.1013|42.3625,-71.0882" ,"mode":"bicycle"}

headers = {
	"X-RapidAPI-Key": "0389397f47mshf84448269e49d01p1378d8jsnd3f6a8f0d320",
	"X-RapidAPI-Host": "route-and-directions.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())



def create_map(response):
    # Extract coordinates from the json response
    mls = response.json()['features'][0]['geometry']['coordinates']
    lons, lats = zip(*mls[0])  # Unpack latitudes and longitudes into two tuples one lons one lats
    #json file puts lon values first  Cartesian coordinates
    print("Latitude values:", lats)
    print("Longitude values:", lons)
    # Create a Plotly line figure for the map using lat and lon values
    fig = px.line_mapbox(lat=lats,lon=lons,zoom = 10)
    
    # Set up layout for the map
    fig.update_layout(mapbox_style= "open-street-map")
       

    return fig


#creates route map
route_fig = create_map(response)

# Creating main map figure 
main_fig =  px.scatter_mapbox(Map, zoom=10, lon =Map['start station longitude'], lat =Map['start station latitude'], size= Map['tripduration_min'], color=Map['tripduration_min'], text =Map['start station name'], title ="Boston Bike Share Scatter Map") 
#adjusts margins on map, right, top, left, bottom
main_fig.update_layout(margin={"r":0,"t":50,"l":0,"b":10})
main_fig.update_layout(mapbox_style="open-street-map")

# gives access toonly the first trace in route_fig data which contain an array of lat and lon values used in our route plot
first_trace = route_fig.data[0]
# adding the route figure trace to main fig
main_fig.add_trace(go.Scattermapbox(
    #accesses latl/lon trace values in foute_fig data
    lat=first_trace.lat,
    lon=first_trace.lon,
    mode='lines',
    line=dict(color='blue', width=2),
    name='Most Used route'))
print("lat/lon values:", route_fig.data[0])

#opens browser window for map
main_fig.show(renderer='browser')
