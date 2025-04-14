from pathlib import Path
import pandas as pd
import sqlite3

from psycopg2 import connect

# from training.name_data.generat_synthetic_names import load_last_names

# Define file path
names_2010_xlsx = Path("names/Names_2010Census_Top1000.xlsx")

# Load the Excel file with correct header row (second row in Excel is index 1)
df = pd.read_excel(names_2010_xlsx, engine="openpyxl", header=2)


# # Print column names
# print("✅ Column names found:")
# for i, col in enumerate(df.columns):
#     print(f"{i}: '{col}'")

# Extract the correct column and rename it to something cleaner
surname_df = df[["SURNAME"]].dropna().copy()
surname_df.columns = ["Surname"]

# Drop last two rows
surname_df = surname_df.iloc[:-2].copy()
surname_df.reset_index(drop=True, inplace=True)


# Database section
db_path = Path('clean_names/clean_surname.db')

# Connect to SQLite database
conn = sqlite3.connect(db_path)

# Write the DataFrame to a table named 'surnames'
surname_df.to_sql('surname', conn, if_exists='replace', index=False)

# Close the connection
conn.close()

print("✅ Surnames saved to SQLite database.")