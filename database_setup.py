import mysql.connector
import csv


DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'Badass#118'  
DB_NAME = 'securecheck'

# --- SQL SCHEMA DEFINITION ---
TABLE_NAME = "traffic_stops"
CREATE_TABLE_QUERY = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    id INT AUTO_INCREMENT PRIMARY KEY,
    stop_date DATE,
    stop_time TIME,
    country_name VARCHAR(100),
    driver_gender VARCHAR(10),
    driver_age_raw INT,
    driver_age INT,
    driver_race VARCHAR(50),
    violation_raw VARCHAR(255),
    violation VARCHAR(255),
    search_conducted BOOLEAN,
    search_type VARCHAR(100),
    stop_outcome VARCHAR(100),
    is_arrested BOOLEAN,
    stop_duration VARCHAR(50),
    drugs_related_stop BOOLEAN,
    vehicle_number VARCHAR(50)
);
"""

def setup_database():
    conn = None
    try:
        
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        
        # 2. Create Database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Database '{DB_NAME}' is ready.")

        # 3. Switch to the new database
        cursor.execute(f"USE {DB_NAME}")

        # 4. Create Table
        cursor.execute(CREATE_TABLE_QUERY)
        print("Table structure verified.")

        # 5. Load Data from CSV
        print("Starting data import...")
        with open('traffic_stops_cleaned.csv', mode='r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)  # Skip header row
            
            # Prepare the SQL INSERT query dynamically
            placeholders = ", ".join(["%s"] * len(headers))
            insert_query = f"INSERT INTO {TABLE_NAME} ({', '.join(headers)}) VALUES ({placeholders})"
            
            # Insert rows
            for row in reader:
                # Convert empty strings to None (NULL) for SQL
                processed_row = [None if x == '' else x for x in row]
                cursor.execute(insert_query, processed_row)
        
        conn.commit()
        print("Data import complete successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    except FileNotFoundError:
        print("Error: 'traffic_stops_cleaned.csv' not found. Run data_preprocessing.py first.")

    finally:
        # Close connection safely
        if conn is not None and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    setup_database()
