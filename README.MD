# Traffic Police Dashboard

Hey, this is my project for the Data Science course! It's a dashboard for traffic police to check vehicle logs and spot high-risk drivers.

Basically, I took a bunch of traffic stop data (CSV file), loaded it into a MySQL database, and then built a simple app to search through it. I didn't use any fancy libraries like Pandas for the logic because I wanted to learn how to do it with just Python lists and loops.

## What it does
- **View Logs:** Shows the last 20 traffic stops so you can see what's happening.
- **Search Vehicle:** You can type in a vehicle number (like `UP76...`) and see every time it was stopped.
- **SQL Reports:** I built a menu where you can run specific reports (like "Top Drug Stops" or "Arrests by Age"). The app runs the SQL query live and shows you the result.
- **High Risk Alerts:** This one is cool—it automatically finds cars that have been stopped more than once using a `HAVING` clause.

## How to run it
1. First, you need to set up the database. Open the `database_setup.py` file and put in your MySQL password (look for `YOUR_PASSWORD`). Then run it:


(This creates the table and loads the CSV data).

2. Then, to start the dashboard, open `app.py` and put your password there too. Then run:

## Files in this folder
- `app.py`: The main dashboard code (contains all the SQL report logic).
- `database_setup.py`: Script to create the database.
- `data_preprocessing.py`: Cleans up the raw CSV file (fixes dates, etc.).
- `traffic_stops.csv`: The raw data.
- `requirements.txt`: The list of python libraries needed.

## Tech used
- Python
- MySQL
- Streamlit (for the website part)

Let me know if you have any questions!
