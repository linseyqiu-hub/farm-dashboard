import pandas as pd
 
# ─────────────────────────────────────────
# 1. LOAD
# ─────────────────────────────────────────
df = pd.read_csv("./data/farmer_advisor_dataset.csv")
pd.set_option('display.max_columns', None) 
 
# ─────────────────────────────────────────
# 2. INSPECT  ← run this first, then comment it out later
# ─────────────────────────────────────────
print("=== SHAPE (rows, columns) ===")
print(df.shape)
#(10000, 10)
 
print("\n=== COLUMN NAMES ===")
print(df.columns.tolist())
# ['Farm_ID', 'Soil_pH', 'Soil_Moisture', 'Temperature_C', 'Rainfall_mm', 'Crop_Type', 'Fertilizer_Usage_kg', 'Pesticide_Usage_kg', 'Crop_Yield_ton', 'Sustainability_Score']
print("\n=== FIRST 5 ROWS ===")
print(df.head())
#    Farm_ID   Soil_pH  Soil_Moisture  Temperature_C  Rainfall_mm Crop_Type  \
# 0        1  7.073643      49.145359      26.668157   227.890912     Wheat   
# 1        2  6.236931      21.496115      29.325342   244.017493   Soybean   
# 2        3  5.922335      19.469042      17.666414   141.110521      Corn   
# 3        4  6.845120      27.974234      17.188722   156.785663     Wheat   
# 4        5  6.934171      33.637679      23.603899    77.859362      Corn   

#    Fertilizer_Usage_kg  Pesticide_Usage_kg  Crop_Yield_ton  \
# 0           131.692844            2.958215        1.576920   
# 1           136.370492           19.204770        3.824686   
# 2            99.725210           11.041066        1.133198   
# 3           194.832396            8.806271        8.870540   
# 4            57.271267            3.747553        8.779317   

#    Sustainability_Score
# 0             51.913649
# 1             47.159077
# 2             50.148418
# 3             89.764557
# 4             51.033941
print("\n=== DATA TYPES ===")
print(df.dtypes)
# === DATA TYPES ===
# Farm_ID                   int64
# Soil_pH                 float64
# Soil_Moisture           float64
# Temperature_C           float64
# Rainfall_mm             float64
# Crop_Type                object 
# Fertilizer_Usage_kg     float64
# Pesticide_Usage_kg      float64
# Crop_Yield_ton          float64
# Sustainability_Score    float64
# dtype: object 
# all columns are numeric except Crop_Type which is categorical (object)
print("\n=== MISSING VALUES (count per column) ===")
print(df.isnull().sum())
# all zeros, no missing values 
print("\n=== BASIC STATS (numeric columns) ===")
print(df.describe().T)
#                         count         mean          std        min  \
# Farm_ID               10000.0  5000.500000  2886.895680   1.000000
# Soil_pH               10000.0     6.499494     0.574181   5.500021
# Soil_Moisture         10000.0    29.988655    11.493376  10.002907
# Temperature_C         10000.0    25.027475     5.769509  15.000186
# Rainfall_mm           10000.0   174.969854    72.860989  50.031967
# Fertilizer_Usage_kg   10000.0   125.212701    43.132645  50.007543
# Pesticide_Usage_kg    10000.0    10.521074     5.535558   1.001370
# Crop_Yield_ton        10000.0     5.489634     2.608809   1.000323
# Sustainability_Score  10000.0    50.213200    28.667146   0.003672

#                               25%          50%          75%           max
# Farm_ID               2500.750000  5000.500000  7500.250000  10000.000000
# Soil_pH                  6.003992     6.495380     6.993481      7.499762
# Soil_Moisture           20.027802    29.862527    40.052369     49.994713
# Temperature_C           20.078612    24.955117    30.053313     34.999673
# Rainfall_mm            111.786631   174.468002   237.812507    299.986192
# Fertilizer_Usage_kg     87.945625   125.188012   162.619398    199.991631
# Pesticide_Usage_kg       5.675684    10.619785    15.330758     19.999099
# Crop_Yield_ton           3.218402     5.490626     7.740585      9.999638
# Sustainability_Score    25.974568    50.234210    74.938267     99.994545
print("\n=== UNIQUE VALUES (useful for category columns) ===")
print(df["Crop_Type"].unique())
print("Total unique:", df["Crop_Type"].nunique())
# ['Wheat' 'Soybean' 'Corn' 'Rice']
# Total unique: 4 
 
# ─────────────────────────────────────────
# 3. CLEAN  ← edit these based on what you find above
# ─────────────────────────────────────────
 
# Drop rows where ANY value is missing
df = df.dropna() 
# Reset index after filtering (optional but clean habit)
df = df.reset_index(drop=True)
 
# Round all numeric columns to 2 decimal places
# Reason: synthetic data has 6 decimal noise from random() — real agricultural
# instruments only measure to 1-2 decimals, so this looks more realistic
cols_to_round = [col for col in df.columns if col != "Crop_Yield_ton"]
df[cols_to_round] = df[cols_to_round].round(2)
# ─────────────────────────────────────────
# 4. VERIFY  ← quick sanity check after cleaning
# ─────────────────────────────────────────
print("\n=== AFTER CLEANING ===")
print("Shape:", df.shape)
print("Missing values:", df.isnull().sum().sum())  # should be 0
print(df.head())
 
 
# ─────────────────────────────────────────
# 5. SAVE
# ─────────────────────────────────────────
df.to_csv("./data/cleaned.csv", index=False)
