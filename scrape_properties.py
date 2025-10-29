import pandas as pd
import sqlite3
import numpy as np
import re

DB_FILE = 'real_estate.db'
CSV_FILE = 'Bengaluru_House_Data.csv'

def clean_sqft(raw_sqft):
    try:
        val = str(raw_sqft).strip()
        if '-' in val:
            vals = [float(x) for x in val.split('-')]
            return np.mean(vals)
        else:
            num = re.findall(r"[0-9]+\.?[0-9]*", val)
            return float(num[0]) if num else None
    except:
        return None

def clean_bedrooms(size_str):
    match = re.search(r'\d+', str(size_str))
    if match:
        return int(match.group())  
    return None

def price_to_rupees(price):
    try:
        return float(price) * 100000
    except:
        return None

print(f"PHASE 1: Starting Data Cleaning engine...")
print(f"Loading raw data from '{CSV_FILE}'...")

try:
    df = pd.read_csv(CSV_FILE)
    columns_needed = ['area_type', 'availability', 'location', 'size', 'total_sqft', 'bath', 'balcony', 'price']
    df = df[columns_needed]

    print("Data loaded. Cleaning chestunnanu...")

    df['bedrooms'] = df['size'].apply(clean_bedrooms)
    df['total_sqft_clean'] = df['total_sqft'].apply(clean_sqft)
    df['price_rupees'] = df['price'].apply(price_to_rupees)
    df['price_per_sqft'] = (df['price_rupees'] / df['total_sqft_clean']).round(2)

    for col in ['bath', 'balcony', 'bedrooms']:
        df[col] = df[col].fillna(df[col].median())

    df = df.dropna(subset=['price_rupees', 'total_sqft_clean', 'price_per_sqft'])
    df = df[df['total_sqft_clean'] > 300]

    df.insert(0, 'serial_no', range(1, 1 + len(df)))

    print("Cleaned Data Sample (first 5 rows):")
    print(df.head())

    print(f"\nSaving clean data to SQLite database ({DB_FILE})...")
    conn = sqlite3.connect(DB_FILE)
    df.to_sql('properties', conn, if_exists='replace', index=False)
    conn.close()

    print(f"Success! Data antha '{DB_FILE}' file lo save ayindi.")
    print("PHASE 1 COMPLETE.")

except FileNotFoundError:
    print(f"ERROR: '{CSV_FILE}' file dorakaledu.")
    print(f"Please check: File ni '{CSV_FILE}' ga rename chesava?")
except Exception as e:
    print(f"An unexpected error occurred: {e}")








