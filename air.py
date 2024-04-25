import pandas as pd
import time
import datetime
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
        host="database",
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
df_open_cases["Intake Date"] = pd.to_datetime(
    df_open_cases["Intake Date"])
df_open_cases["Outcome Date"] = pd.to_datetime(
    df_open_cases["Outcome Date"])

# Animals in Residence by Date
start_date = df_open_cases["Intake Date"].min()
end_date = datetime.datetime.now()
date_list = {}

while start_date <= end_date:
    loop_date = start_date.strftime('%Y-%m-%d')
    date_list[loop_date] = 0
    start_date += datetime.timedelta(days=1)

for k, v, in date_list.items():
    date_list[k] = ((pd.isnull(df_open_cases['Outcome Date']) &
                    (df_open_cases["Intake Date"] <= k)) |
                    ((df_open_cases["Intake Date"] <= k) &
                    (df_open_cases['Outcome Date'] > k))).sum()
df_dates = pd.DataFrame.from_dict(
    date_list, orient='index', columns=['Animals in Residence'])

tuple_dates = [(k, v) for k, v in date_list.items()]
records_list_template = ','.join(['%s'] * len(data))
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
    VALUES {}
    ON CONFLICT ("Date")
    DO UPDATE SET
        ("Date", "Animals in Residence")
""".format(records_list_template)

# Execute the insert statement
cur.execute(insert_stmt, tuple_dates)

# Commit the changes to the database
conn.commit()

# Close the cursor and connection
cur.close()