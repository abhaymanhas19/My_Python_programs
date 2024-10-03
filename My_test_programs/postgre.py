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
query = "SELECT * FROM users_projectquery WHERE id = 2694"

# Fetch data into a DataFrame
df = pd.read_sql_query(query, conn)

# Export DataFrame to JSON
df.to_json('output_2694.json', orient='records', lines=True)

conn.close()
