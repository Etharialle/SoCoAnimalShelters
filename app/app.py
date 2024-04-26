import streamlit as st
import matplotlib.pyplot as plt
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

### Functions ###


# Create a dataframe from a CSV file


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

def fetch_air():
    #url = "https://raw.githubusercontent.com/Etharialle/SoCoAnimalShelters/main/datasets/asio_animal_in_residence.csv"
    #df_air = pd.read_csv(url, on_bad_lines='skip').replace("'", "", regex=True)
    #return df_air

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

    cur.execute("SELECT * FROM asio_animal_in_residence")
    df_air = pd.DataFrame(cur.fetchall(), columns=[desc[0] for desc in cur.description])

    cur.close()
    conn.close()
    return df_air

# Count the number of each type of animal with open cases


def count_open_cases(df):
    num_open_dog_cases = df[(df['Outcome Date'] == '') &
                            (df['Type'].str.contains(
                                'dog', na=False, case=False))].shape[0]
    num_open_cat_cases = df[(df['Outcome Date'] == '') &
                            (df['Type'].str.contains(
                                'cat', na=False, case=False))].shape[0]
    num_open_other_cases = df[(df['Outcome Date'] == '') &
                              (df['Type'].str.contains(
                                  'other', na=False, case=False))].shape[0]
    return num_open_dog_cases, num_open_cat_cases, num_open_other_cases

# Pie chart formatting


def autopct_format(values):
    def my_format(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{v:d}'.format(v=val)
    return my_format


### End of Functions ###


def main():
    st.set_page_config(layout="wide", page_title="Sonoma County Animal Shelter Analytics", page_icon="./assets/img/etharialle.ico")
    st.title("Sonoma County Animal Shelter Analytics")
    st.header("Open Cases by Animal Type")
    with st.sidebar:
        st.subheader("About:")
        st.markdown("SoCo Data makes available the data on intakes and outcomes of animals through the shelters in the county.  Here we explore different trends so we can look at presriptive and predictive analytics.")

    col1, col2 = st.columns(2)
    df = fetch_data()
    df_air = fetch_air()

    # Column 1 Start
    with col1:
        # Count the number of each type of animal with open cases
        num_open_dog_cases, num_open_cat_cases, num_open_other_cases = count_open_cases(
            df)

        # Organize data for pyplot
        labels = ['Dogs', 'Cats', 'Others']
        sizes = [num_open_dog_cases, num_open_cat_cases, num_open_other_cases]
        explode = (0, 0, 0)

        # create a figure and set different background
        fig = plt.figure()
        fig.patch.set_facecolor('#30646C')

        # Change color of text
        plt.rcParams['text.color'] = 'white'

        # autopct = '%1.1f%%' for percentage values
        # autopct=autopct_format(sizes) for values instead percent
        plt.pie(sizes, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)

        st.pyplot(fig)
    # Column 1 Start
    with col2:
        st.markdown("""
            ### 🐕 dogs: {} """.format(num_open_dog_cases)
                    )
        st.markdown("""
            ### 🐈 cats: {} """.format(num_open_cat_cases)
                    )
        st.markdown("""
            ### 🐎 others: {} """.format(num_open_other_cases)
                    )

        # st.dataframe(df_air.sort_values(by='Date', ascending=False))
    st.header("Animals in Residence by Date")
    st.line_chart(data=df_air, x='Date', y='Animals in Residence')
    chart_display = st.radio("Select one:", ["Outcome Types", "Intake Types", "Average days in shelter by Outcome",
                                             "Average days in shelter by animal type"], horizontal=True)
    if chart_display == "Outcome Types":
        df_outcomes = df.groupby("Outcome Type")["Impound Number"].count()
        df_outcomes.rename('Total Outcomes', inplace=True)
        st.dataframe(df_outcomes)
        st.bar_chart(data=df_outcomes, y='Total Outcomes')

    elif chart_display == "Intake Types":
        df_intakes = df.groupby("Intake Type")["Impound Number"].count()
        df_intakes.rename('Total Intakes', inplace=True)
        st.dataframe(df_intakes)
        st.bar_chart(data=df_intakes, y='Total Intakes')

    elif chart_display == "Average days in shelter by Outcome":
        #avg_days_outcome_type = {}
        avg_days_outcome_type = df.groupby("Outcome Type")["Days in Shelter"].mean()
        st.dataframe(avg_days_outcome_type)
        st.bar_chart(data=avg_days_outcome_type, y='Days in Shelter')
    
    elif chart_display == "Average days in shelter by animal type":
        #avg_days_outcome_type = {}
        avg_days_animal_type = df.groupby("Type")["Days in Shelter"].mean()
        st.dataframe(avg_days_animal_type)
        st.bar_chart(data=avg_days_animal_type, y='Days in Shelter')

if __name__ == "__main__":
    main()
