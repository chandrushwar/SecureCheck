import csv
from datetime import datetime

def clean_date(date_str):
    """Converts MM/DD/YYYY to YYYY-MM-DD for MySQL"""
    if not date_str: return None
    try:
        return datetime.strptime(date_str, "%m/%d/%Y").strftime("%Y-%m-%d")
    except ValueError:
        return None 

def clean_bool(val):
    """Converts TRUE/FALSE text to 1/0 integers"""
    if not val: return 0
    return 1 if str(val).upper() == 'TRUE' else 0

def clean_int(val):
    """Safely converts string to integer, default to 0"""
    if not val: return 0
    try:
        return int(float(val))
    except ValueError:
        return 0

input_file = 'traffic_stops.csv'
output_file = 'traffic_stops_cleaned.csv'


bool_cols = ['search_conducted', 'is_arrested', 'drugs_related_stop']
int_cols = ['driver_age', 'driver_age_raw']
date_col = 'stop_date'

with open(input_file, mode='r', encoding='utf-8-sig', newline='') as infile, \
     open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
    
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames
    
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    
    print("Processing CSV rows...")
    
    for row in reader:
        cleaned_row = row.copy()
        
  
        cleaned_row[date_col] = clean_date(row[date_col])
 
        for col in int_cols:
            cleaned_row[col] = clean_int(row[col])

     
        for col in bool_cols:
            cleaned_row[col] = clean_bool(row[col])

     
        for col in fieldnames:
            if col not in bool_cols and col not in int_cols and col != date_col:
                if not row[col] or row[col].strip() == '':
                    cleaned_row[col] = 'Unknown'

        writer.writerow(cleaned_row)

print(f"Done! Cleaned data saved to '{output_file}'")

