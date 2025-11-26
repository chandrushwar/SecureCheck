# Traffic Police Dashboard

This's a dashboard for traffic police to check vehicle logs and spot high-risk drivers.
Loaded cleaned traffic stop data into a MySQL database and then built a an app to search through it. Runs on SQL and python.

# What it does
View Logs: Shows the last 20 traffic stops.
Search Vehicle: type in a vehicle number and see every time it was stopped.
SQL Reports: a menu where you can run specific reports , The app runs the SQL query live and shows you the result.
High Risk Alerts:  finds cars that have been stopped more than once.

## Files in this folder
- app.py: The main dashboard code (contains all the SQL report logic).
- database_setup.py: Script to create the database.
- data_preprocessing.py: Cleans up the raw CSV file (fixes dates, etc.).
- traffic_stops.csv: The raw data.
- requirements.txt: The list of python libraries needed.

## Tech used
- Python
- MySQL
- Streamlit
