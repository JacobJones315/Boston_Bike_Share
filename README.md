# Forecasting and Optimizing Boston Bluebikes Bike Sharing Company

## Background 
* Bluebikes is the public bike share program serving Metro Boston, boasting a fleet of over 4,000 bikes stationed at more than 400 locations across Arlington, Boston, Brookline, Cambridge, Chelsea, Everett, Newton, Revere, Salem, Somerville, and Watertown. Offering a convenient, affordable, and enjoyable transportation solution, Bluebikes is perfect for short journeys around the city. In this project week looked at data over a two year period from 2019-2020.

## Problem Statement 
* Given the evolving urban mobility landscape and increasing competition in the bike-sharing industry, how can Blue Bikes strategically expand its service area and enhance revenue streams in the city of Boston?
* What data-driven insights from current usage patterns, demographic trends, and operational metrics can inform targeted strategies for market expansion, thereby ensuring sustainable growth and increased market share?
* How can Blue Bikes increase its subscriber base and extend its operational footprint?
* With particular emphasis on leveraging insights from existing usage patterns, demographic trends, and operational data, what targeted strategies can be developed to not only broaden the market presence of Blue Bikes but also deepen customer engagement and loyalty?

## Methods
* Methodology 1
    * Goal: Forecast # of customers and subscribers that will use the Blue Bikes service in the upcoming year, test a regression based forecasting model and a holt winters triple exponential smoothing model
    * How? → Using time series forecasting (using Python), we will analyze patterns and trends in historical data (2019 and 2020) to make predictions for the future
    * Why? → Will allow Blue Bikes to make informed decisions and plan resources
* Methodology 2
    * Goal: Extract insights to develop a strategy for Blue Bikes to stock stations appropriately and expand docking stations in areas with high demand potential
    * How? → Capacity planning using optimization models, trend and forecasting analysis of the most and least popular start and end stations (using Python) to reveal high demand areas and underserved locations
    * Why? → Blue Bikes can have a sufficient number of bikes at each station so that the probability that a customer is able to get a bike is above a certain threshold.
* Methodology 3
    * Goal: Analyze the data to understand usage patterns between customers and subscribers
    * How? → Complete analysis on customers and subscribers using
    * Why? → Blue Bikes can understand which segment to target
 
## Summary
* Methodology 1
   * Based on our analysis, we recommend Blue Bikes to adopt a Holt-Winters triple exponential smoothing model for forecasting over a regression-based approach. Our evaluation revealed a significantly lower mean absolute percentage error (MAPE) with the Holt-Winters model, indicating enhanced forecasting accuracy. By weighting both actual and forecasted sales data, this approach reliably predicts sales for both subscribers and customers. This choice was made due to the model's ability to capture seasonality and trends in the data effectively. Implementing this model will enable Blue Bikes to make informed decisions regarding bike allocation, ultimately improving customer satisfaction and maximizing revenue.
*  Methodology 2
   * Blue Bikes can leverage our dynamic dashboard to gain real-time insights into inflow and outflow patterns at each station, enabling them to optimize bike stock levels and make informed decisions about installing temporary pop-up stations where needed. By accurately determining the optimal number of bikes to have on hand at each station, Blue Bikes can significantly enhance subscriber/customer satisfaction by reducing the risk of stockouts. This not only improves the overall user experience but also helps prevent potential revenue loss from customers turning to other bike sharing companies due to unavailability of bikes. Additionally, the dynamic dashboard allows for efficient allocation of resources, leading to improved operational efficiency and service reliability. Blue Bikes can fully harness the potential of the dynamic dashboard to drive business success and deliver exceptional service to their customers.
* Methodology 3
   * Based on our analysis of subscribers and customers, we've found that the majority of Bluebikes bike sharing service users are subscribers. To develop a targeted marketing campaign aimed at acquiring new subscribers, we conducted a breakdown of subscriber/customer numbers per zip code in Boston. We propose offering a free trial period to customers in the zip codes with the highest customer concentration. This initiative will allow them to experience the benefits of a Bluebikes subscription firsthand, thereby expanding our subscriber base and boosting revenue

 ## Procedure

 * Forecasting
   * Imported bike trip data for the years 2019 and 2020, converting the 'starttime' column to datetime format.
   * Segmented the data into separate dataframes for subscribers and customers.
   * Extracted key features such as start times and utilized the Pandas grouper method coupled with count to aggregate weekly sales.
   * Visualized the weekly sales data on a line graph, identifying observable trends and seasonality patterns.
   * I imported the ExponentialSmoothing function from the statsmodel.tsa.holtwinters library.
   * Proceeded to construct separate additive and multiplicative trend and seasonality models to generate forecasts.
   * Calculated absolute percentage errors for actual and forecasted sales for each model.
   * Computed Mean Absolute Percentage Error (MAPE) to assess forecast accuracy, determining that the multiplicative trend and seasonality model outperformed the additive model.
   * Utilized the superior multiplicative model to forecast sales for both subscribers and customers 12 weeks into the future.
* Optimization
   * Imported bike trip data for the years 2019 and 2020, converting the 'starttime' column to datetime format.
   * Converted start time into datetime format and extracted the hour.
   * Grouped my dataframe by key features such as start station id, start station name, month, day of week, and hour and found the size of the data frame which indicated the number of outgoing rides per hour from each station. Then found the number of trip counts per hour and the standard deviation for each hour
   * Grouped the trip data by start station, month, day of the week, and hour to calculate the number of trips leaving each station per hour (hourly_trips).
   * Grouped the trip data by end station, month, day of the week, and hour to calculate the number of trips arriving at each station per hour (hourly_trips).
   * Calculated the average and standard deviation of trips leaving each station per hour (detailed_outflow_stats).
   * Calculated the average and standard deviation of trips arriving at each station per hour (detailed_inflow_stats).
   * Merged the outflow and inflow datasets based on common columns to analyze net demand and optimal bike stocking levels (data_merged).
   * Calculated net demand by subtracting the average outflow trips from the average inflow trips.
   * Calculated the standard deviation of net demand.
   * Determined the optimal number of bikes to stock at each station per hour based on service level and z-score.
   * Created a dynamic dashboard that allows you to select the station id and month and get the optimal hourly saftey stock levels 
   * Defined a function named plot_bike_stock_for_month that takes two parameters: station_id and month.
   * Created a list days_of_week containing the names of all seven days.
   * Iterated over each day of the week using a for loop.
   * Enumerated the loop starting from 1 using enumerate(days_of_week, 1).
   * Filtered the merged data (data_merged) to select rows corresponding to the specified station_id, month, and day_of_week.
   * This filtering isolates data for the specific station, month, and day of the week.
   * Sorted the filtered data by the 'hour' column to ensure that the line plot shows the variation in optimal bike stock over hours of the day.
   * Configured subplots within the main figure for each day of the week.
   * The subplot layout is arranged in a grid format using plt.subplot().
   * Plotted a line graph showing the variation of 'optimal_bikes_stock' (optimal number of bikes to stock) over hours of the day.
   * Used sns.lineplot() to create the line plot, specifying the x-axis as 'hour' and the y-axis as 'optimal_bikes_stock'.
   * Call the function with a specific station ID and month plot_bike_stock_for_month(68, 2). 





