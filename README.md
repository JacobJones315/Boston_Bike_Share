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
