# Spent

## Summary

**Spent** is a practical and versatile budget tracking and money management app, offering users an easy-to-read visualization of their finances and a detailed log of their spending habits. With Spent, you can create budgets, set spending goals, and store information about your recent purchases.


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

Spent is an app built on a Flask server with a PostgreSQL database. SQLAlchemy as the ORM used to interact with this database. The front end templating uses Jinja2, the HTML was built using Bootstrap, and the Javascript uses JQuery and AJAX to interact with the backend. The graphs are rendered using Chart.js, a free Javascript charting library. The map is built using the Google Maps API, which works in tandem with the Shippo package tracking API.


## Features

![alt text](https://github.com/emilydowgialo/Spent/blob/master/static/spent-login-screenshot.png "Spent Login")


The interactive dashboard features graphs, which segment the user’s expenditures into categories, and auto-updating widgets, which illustrate spending metrics and statistics. The user enters budgets for categories along with a date range that is used to display spending stats over that particular time period. The bar graph and the donut chart show stats based on the user's spending habits within the last 30 days. The bar graph shows the average amount spent per category, while the donut chart displays the total amount spent. The Budget Remaining widget's progress bars graphically represent the remaining money in the user's budget. Two more widgets display the average and total amounts spent per category within the specified date range. Everything on the dashboard updates in real time as the user adds a new budget or a new expenditure.


![alt text](https://github.com/emilydowgialo/Spent/blob/master/static/spent-dashboard-screenshot.png "Spent Login")


Spent's dynamic package tracking feature monitors online purchases, which displays the last place a package was scanned, its delivery status, and plots its current location on a map. When the user saves a new purchase, they are given the option to input tracking information. If the user has tracking information saved, a paper airplane icon is displayed next to the corresponding purchase, and the user simply has to click on the icon to track their package.


![alt text](https://github.com/emilydowgialo/Spent/blob/master/static/spent-map-screenshot.png "Spent Login")


Spent is a one-page dashboard. There is beauty and functionality in simplicity, and the user's flow is kept direct and clean. The user inputs budget and expenditure information in modal window forms that do not take them away from the main dashboard, keeping the user experience focused.


![alt text](https://github.com/emilydowgialo/Spent/blob/master/static/spent-modal-screenshot.png "Spent Login")


## Version 2.0

- **More chart control:** Ability to customize the categories and timeframes the charts display
- **Badges:** Badges for certain milestones, such as staying under budget for a given period of time
- **Password hashing:** Passwords will be hashed before being saved to the database


## About the Developer

Spent was created by Emily Dowgialo, a software engineer in San Francisco, CA. Learn more about the developer on [LinkedIn](https://www.linkedin.com/in/emilydowgialo).
