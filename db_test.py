import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv(override=True)
db_name = os.getenv("db_name")
db_user = os.getenv("db_user")
db_pass = os.getenv("db_pass")

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database=db_name,
    user=db_user,
    password=db_pass,
)
# Create a cursor object to execute queries
cur = conn.cursor()

cur.execute("SELECT * FROM asio")
df = pd.DataFrame(cur.fetchall(), columns=[desc[0] for desc in cur.description])
print(df.head())
print(df.dtypes)
cur.close()
conn.close()
