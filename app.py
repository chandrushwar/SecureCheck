import streamlit as st
import mysql.connector

# --- TITLE ---
st.title("Traffic Police Dashboard")

# --- DATABASE CONNECTION ---
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Badass#118", 
        database="securecheck"
    )
    cursor = mydb.cursor()
except Exception as e:
    st.error(f"Database Connection Failed: {e}")
    st.stop()

# --- SIDEBAR ---
st.sidebar.title("Menu")
menu = st.sidebar.radio("Go to:", ["View Logs", "Search Vehicle", "SQL Reports", "High Risk Alerts"])

# --- 1. VIEW LOGS ---
if menu == "View Logs":
    st.header("Recent Traffic Stops")
    
    try:

        cursor.execute("""
            SELECT stop_date, stop_time, vehicle_number, 
                   driver_gender, violation, stop_outcome 
            FROM traffic_stops 
            ORDER BY stop_date DESC LIMIT 20
        """)
        data = cursor.fetchall()
        
        if data:
            
            headers = ["Date", "Time", "Vehicle", "Gender", "Violation", "Outcome"]
            
            table_data = [headers] + [list(row) for row in data]
            
            for i in range(1, len(table_data)):
                table_data[i][1] = str(table_data[i][1])

            st.table(table_data)
            
        else:
            st.write("No logs found.")
                
    except Exception as e:
        st.error(f"Error fetching logs: {e}")


# --- 2. SEARCH VEHICLE ---
elif menu == "Search Vehicle":
    st.header("Search Vehicle")
    v_num = st.text_input("Enter Vehicle Number:")
    
    if st.button("Search"):
        cursor.execute("SELECT * FROM traffic_stops WHERE vehicle_number = %s", (v_num,))
        results = cursor.fetchall()
        
        if results:
            st.success("Vehicle Found!")
           
            headers = [i[0] for i in cursor.description]
            
         
            for row in results:
                st.write("---")
                for i, val in enumerate(row):
                    st.write(f"**{headers[i]}:** {val}")
        else:
            st.warning("No records found.")

# --- 3. SQL REPORTS ---
elif menu == "SQL Reports":
    st.header("Automated Reports")
    
    choice = st.selectbox("Select Report", [
        "1. Top 10 Drug Stops (Vehicle)",
        "2. Arrest Rate by Age",
        "3. Busiest Time of Day",
        "4. Country-wise Drug Rates",
        "5. Top Search Violations",
        "6. Complex: Yearly Breakdown",
        "7. Complex: High Search Rate Violations",
        "8. Complex: Top 5 Arrest Violations"
    ])
    
    if st.button("Run Report"):
        sql = ""
        
        if "1." in choice:
            sql = "SELECT vehicle_number, COUNT(*) FROM traffic_stops WHERE drugs_related_stop = 1 GROUP BY vehicle_number LIMIT 10"
        elif "2." in choice:
            sql = "SELECT driver_age, COUNT(*) FROM traffic_stops WHERE is_arrested = 1 GROUP BY driver_age LIMIT 10"
        elif "3." in choice:
            sql = "SELECT stop_time, COUNT(*) FROM traffic_stops GROUP BY stop_time ORDER BY COUNT(*) DESC LIMIT 10"
        elif "4." in choice:
            sql = "SELECT country_name, COUNT(*) FROM traffic_stops WHERE drugs_related_stop = 1 GROUP BY country_name"
        elif "5." in choice:
            sql = "SELECT violation, SUM(search_conducted) FROM traffic_stops GROUP BY violation ORDER BY SUM(search_conducted) DESC"
        elif "6." in choice:
            sql = "SELECT YEAR(stop_date), COUNT(*) FROM traffic_stops GROUP BY YEAR(stop_date)"
        elif "7." in choice:
            sql = "SELECT violation, SUM(search_conducted)/COUNT(*) as rate FROM traffic_stops GROUP BY violation ORDER BY rate DESC LIMIT 5"
        elif "8." in choice:
            sql = "SELECT violation, SUM(is_arrested) FROM traffic_stops GROUP BY violation ORDER BY SUM(is_arrested) DESC LIMIT 5"
            
        
        try:
            cursor.execute(sql)
            res = cursor.fetchall()
            
            if res:
                st.table(res)
            else:
                st.write("No data returned.")
        except Exception as e:
            st.error(f"Query Failed: {e}")

# --- 4. HIGH RISK ALERTS ---
elif menu == "High Risk Alerts":
    st.header("High Risk Vehicles")
    st.write("Vehicles stopped multiple times:")
    
    try:
        cursor.execute("SELECT vehicle_number, COUNT(*) FROM traffic_stops GROUP BY vehicle_number HAVING COUNT(*) > 1")
        res = cursor.fetchall()
        st.table(res)
    except Exception as e:
        st.error(f"Error: {e}")

# Close DB
cursor.close()
mydb.close()
