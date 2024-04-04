import pandas as pd
import requests
import json
import psycopg2

# Initialize DataFrame
df = pd.DataFrame(columns=["name", "type", "breed", "color", "sex", "size", "date_of_birth", "impound_number", "kennel_number", "id", "intake_date", "outcome_date", "days_in_shelter",
                  "intake_type", "intake_subtype", "outcome_type", "outcome_subtype", "intake_condition", "outcome_condition", "intake_jurisdiction", "outcome_jurisdiction", "zip_code"])

# SoCo Data Endpoint
url = 'https://data.sonomacounty.ca.gov/resource/924a-vesw.json?$order=impound_number DESC&$limit=50'
response = requests.get(url)
print(response)

new_data = json.loads(response.text)
df_new = pd.DataFrame(data=new_data)
df_insert = pd.concat([df, df_new], axis=0)

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    host="socodata.cps8aw0cuijp.us-east-2.rds.amazonaws.com",
    port=5432,
    database="postgres",
    user="postgres",
    password="sierra42",
)
# Create a cursor object to execute queries
cur = conn.cursor()

# Insert SQL Statement
insert_stmt = """
    INSERT INTO animal_shelter_intake_and_outcome ("Name", "Type", "Breed", "Color", "Sex", "Size", "Date Of Birth", "Impound Number", "Kennel Number", "Animal ID", "Intake Date", "Outcome Date", "Days in Shelter", "Intake Type", "Intake Subtype", "Outcome Type", "Outcome Subtype", "Intake Condition", "Outcome Condition", "Intake Jurisdiction", "Outcome Jurisdiction", "Outcome Zip Code", "Location", "Count")
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT ("Impound Number")
    DO UPDATE SET
        ("Name", "Type", "Breed", "Color", "Sex", "Size", "Date Of Birth", "Kennel Number", "Animal ID", "Intake Date", "Outcome Date", "Days in Shelter", "Intake Type", "Intake Subtype", "Outcome Type", "Outcome Subtype", "Intake Condition", "Outcome Condition", "Intake Jurisdiction", "Outcome Jurisdiction", "Outcome Zip Code", "Location", "Count") = (EXCLUDED."Name", EXCLUDED."Type", EXCLUDED."Breed", EXCLUDED."Color", EXCLUDED."Sex", EXCLUDED."Size", EXCLUDED."Date Of Birth", EXCLUDED."Kennel Number", EXCLUDED."Animal ID", EXCLUDED."Intake Date", EXCLUDED."Outcome Date", EXCLUDED."Days in Shelter", EXCLUDED."Intake Type", EXCLUDED."Intake Subtype", EXCLUDED."Outcome Type", EXCLUDED."Outcome Subtype", EXCLUDED."Intake Condition", EXCLUDED."Outcome Condition", EXCLUDED."Intake Jurisdiction", EXCLUDED."Outcome Jurisdiction", EXCLUDED."Outcome Zip Code", EXCLUDED."Location", EXCLUDED."Count")
"""

test = df_insert.values.tolist()
# print(type(test[0][23]))
# print()
# for i in range(len(test[0])):
#    print(test[0][i], type(test[0][i]))

for i in range(len(test)):
    if isinstance(test[i][21], str) and isinstance(test[i][22], dict):
        lat = test[i][22]['latitude']
        long = test[i][22]['longitude']
        zip = test[i][21]
        loc = zip + '(' + lat + ', ' + long + ')'
        # print(loc)
        test[i][22] = loc
    else:
        print("null found")
for i in range(len(test)):
    for j in range(len(test[i])):
        if isinstance(test[i][j], float):
            test[i][j] = ''
        # print(type(test[i][j]))
# print(test)
# df2 = pd.DataFrame(test)

cur.executemany(insert_stmt, test)

# Commit the changes to the database
conn.commit()

# Close the cursor and connection objects
cur.close()
conn.close()