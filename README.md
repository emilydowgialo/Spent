# Spent

## Summary

**Spent** is a practical and versatile budget tracking, money management app, offering users an easy-to-read visualization of their finances and a detailed log of their spending habits. With Spent, you can create budgets, set spending goals, and store information about your recent purchases.


## Technologies

**Tech Stack:**

- Python
- Flask
- SQLAlchemy
- Jinja2
- HTML
- CSS
- Javascript
- JQuery
- AJAX
- JSON
- Bootstrap
- Google Maps API
- Shippo API

Spent is a Flask app built on a Flask server with a PostgreSQL database, with SQLAlchemy as the ORM used to interact with this database. The front end templating uses Jinja. HTML was built using Bootstrap. The Javascript uses JQuery and AJAX to interact with the backend so everything updates in real time. The graphs displaying total and average amount spent are rendered using Chart.js, a free Javascript charting library. The map is built using the Google Maps API, which interacts with the Shippo package tracking API.


## Features

![alt text](https://github.com/emilydowgialo/Spent/blob/master/static/spent-login-screenshot.png "Spent Login")


The interactive dashboard features graphs, which segment the user’s expenditures into categories, and auto updating widgets, which illustrate spending metrics and statistics. The user enters budgets for categories along with a date range. The user's spending stats are tabulated based on this date range, and graphically shows the user how much they have left in their budget, as well as the average and total amount they have spent.


![alt text](https://github.com/emilydowgialo/Spent/blob/master/static/spent-dashboard-screenshot.png "Spent Login")


Online purchases can be monitored with Spent’s dynamic package tracking feature, which displays the last place a package was scanned, its delivery status, and plots its current location on a map.


![alt text](https://github.com/emilydowgialo/Spent/blob/master/static/spent-map-screenshot.png "Spent Login")


Spent is a one-page dashboard. There is beauty and functionality in simplicity, and the user's flow is kept direct and clean. The user inputs budget and expenditure information in modal window forms that do not take them away from the main dashboard, keeping their experience focused.


![alt text](https://github.com/emilydowgialo/Spent/blob/master/static/spent-modal-screenshot.png "Spent Login")


## Version 2.0

Spent 2.0 will give users the ability to toggle between which categories and timeframes to display on the charts. It will also be gamified - users will receive badges for certain milestones, such as staying under budget for a given period of time.


## About the Developer

Spent was created by Emily Dowgialo, a software engineer in San Francisco, CA. Learn more about the developer on [LinkedIn](https://www.linkedin.com/in/emilydowgialo).
