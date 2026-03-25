import pandas as pd
import sqlite3
 
# ─────────────────────────────────────────
# 1. CONNECT (creates data.db if it doesn't exist)
# ─────────────────────────────────────────
conn = sqlite3.connect("data.db")
 
 
# ─────────────────────────────────────────
# 2. LOAD cleaned data
# ─────────────────────────────────────────
df = pd.read_csv("./data/cleaned.csv")
cursor = conn.cursor()

# manually define table schema with Farm_ID as primary key
cursor.execute("""
    CREATE TABLE IF NOT EXISTS farm_data (
        Farm_ID              INTEGER PRIMARY KEY,
        Soil_pH              REAL,
        Soil_Moisture        REAL,
        Temperature_C        REAL,
        Rainfall_mm          REAL,
        Crop_Type            TEXT,
        Fertilizer_Usage_kg  REAL,
        Pesticide_Usage_kg   REAL,
        Crop_Yield_ton       REAL,
        Sustainability_Score REAL
    )
""")
conn.commit()


# ─────────────────────────────────────────
# 3. PUSH to SQLite
# if_exists="replace" → drops and recreates the table every time you run this
# if_exists="append"  → adds rows to existing table (don't use this for now)
# index=False         → don't write pandas row numbers as a column
# ─────────────────────────────────────────
df.to_sql("farm_data", conn, if_exists="replace", index=False)
 
 
# ─────────────────────────────────────────
# 4. VERIFY — query it back to confirm it worked
# ─────────────────────────────────────────
result = pd.read_sql("SELECT * FROM farm_data LIMIT 5", conn)
print("=== FIRST 5 ROWS FROM DB ===")
print(result)
 
result2 = pd.read_sql("SELECT COUNT(*) AS total_rows FROM farm_data", conn)
print("\n=== ROW COUNT ===")
print(result2)
 
 
# ─────────────────────────────────────────
# 5. CLOSE connection
# ─────────────────────────────────────────
conn.close()
print("\n data.db ready")