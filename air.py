import pandas as pd
import time
import datetime
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv(override=True)
db_name = os.getenv("db_name")
db_user = os.getenv("db_user")
db_pass = os.getenv("db_pass")


def fetch_data():
    #url = "https://raw.githubusercontent.com/Etharialle/SoCoAnimalShelters/main/datasets/asio.csv"
    #df = pd.read_csv(url, on_bad_lines='skip').replace("'", "", regex=True)
    #return df
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

    cur.close()
    conn.close()
    return df


df = fetch_data()
# Ensure 'Intake Date' is a datetime type
df["Intake Date"] = pd.to_datetime(
    df["Intake Date"])
df["Outcome Date"] = pd.to_datetime(
    df["Outcome Date"])

# Animals in Residence by Date
start_date = df["Intake Date"].min()
end_date = datetime.datetime.now()
date_list = {}

while start_date <= end_date:
    loop_date = start_date.strftime('%Y-%m-%d')
    date_list[loop_date] = 0
    start_date += datetime.timedelta(days=1)

for k, v, in date_list.items():
    date_list[k] = ((pd.isnull(df['Outcome Date']) &
                    (df["Intake Date"] <= k)) |
                    ((df["Intake Date"] <= k) &
                    (df['Outcome Date'] > k))).sum()
df_dates = pd.DataFrame.from_dict(
    date_list, orient='index', columns=['Animals in Residence'])

list_dates = [[str(k), str(v)] for k, v in date_list.items()]

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

# Insert SQL Statement
insert_stmt = """
    INSERT INTO asio_animal_in_residence ("Date", "Animals in Residence")
    VALUES (%s, %s)
    ON CONFLICT ("Date")
    DO UPDATE SET
        "Animals in Residence" = EXCLUDED."Animals in Residence"
"""
# Execute the insert statement
cur.executemany(insert_stmt, list_dates)

# Commit the changes to the database
conn.commit()

# Close the cursor and connection
cur.close()
