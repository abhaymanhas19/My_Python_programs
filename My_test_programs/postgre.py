import psycopg2
import pandas as pd

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="production",
    user="ailyzeadmin",
    password="Database@124",
    host="ailyze-database.postgres.database.azure.com"
)

# Query to fetch data
query = "SELECT * FROM users_projectdata WHERE id = 1927"


cursor=conn.cursor()

cursor.execute(query)
rows = cursor.fetchall()
print(f"Number of records fetched: {len(rows)}")

# Retrieve column names from cursor.description
column_names = [desc[0] for desc in cursor.description]
print(column_names)
# Fetch data into a DataFrame
# df = pd.read_sql_query(query, conn)

# # Export DataFrame to JSON
# df.to_json('output_2694.json', orient='records', lines=True)

conn.close()
