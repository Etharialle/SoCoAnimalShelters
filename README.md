# SoCoAnimalShelters
Data Analytics for Sonoma County Animal Shelters

## Project Background
Open data has become prevalent.  There are datasets from all levels of government, non-profits, universities, and companies (both public and private).  Sonoma County has an open data portal that has 30 datasets (as of April 2024).  The mission from SoCo Data is
> Our goal is to provide open access to data for research and analysis, to spur innovation through the creation of new business opportunities and applications, to improve the efficiency and effectiveness of government services, and for all to learn more about Sonoma County.

The data is provided by the County of Sonoma Department of Health Services and hosted at [SocoData](https://data.sonomacounty.ca.gov/Government/Animal-Shelter-Intake-and-Outcome/924a-vesw/about_data)


## Project Purpose
Provide insights into the operations of the Sonoma County Animal Shelters using data analytics techniques.

## Project Scope
SoCo Data provides some tools for viewing, querying, and visualizing the data on their site, but these tools are limited.  Extracting the data allows for more flexibility when working with the data.

![screenshot of the tools available for interacting the the dataset](/assets/img/soco_data_actions.png)

### ETL (Extract, Transform, Load)

#### Extract
The total dataset is over 20k rows and the API endpoint is limited to 1000 rows at a time.  This dataset is currently active is updated daily. Extracting the data is done in two steps.  Since the API is limited a export to CSV is used to capture the entire dataset at a moment in time.  Going forward new data will be extracted using the API endpoint.

#### Transform
As with the extract process there will be two steps for transforming the data.  The CSV file is cleaned by checking incorrectly input data and identifying the primary key (Impound Number).  New data will be added daily using the API endpoint the response from that endpoint must be cleaned so that it will insert in the PostgreSQL database without errors.

#### Load
The cleaned CSV file is used to create the main table (animal_shelter_intake_and_outcome) in the database.
- [CSV Dataset](/datasets/Animal_Shelter_Intake_and_Outcome_20240402.csv)
- [SQL Script](/sql/animal_shelter_intake_and_outcome_202404032309.sql)

New data is added to the database using the [database_insert.py](database_insert.py) script.  This script performs some transformation to ensure the new data is compatible with the database structure and then inserts the data into the database.

A cron job is used to run the database insert script daily to keep the database in sync with the original data source on SoCo Data.

### Data Visualizations
Visualizations are created using Tableau Public and linked to the project database (hosted on an AWS RDS instance).

Visualizations to create
- [ ] Frequent Fliers (Animal ID duplicates)
- [ ] Euthenasia states
- [ ] Outcome locations
- [ ] Animal Type Breakdown (for "other" need to use "breed" as well)

### Predictive Analytics
TBD

### Prescriptive Analytics (Bonus)
TBD

## Project Architecture

![Project Architecture](/assets/img/network_diagram.svg)

## Resources

### Tools Used
- AWS EC2 (AWS Linux)
- AWS RDS
- VSCode
- Postgresql
- Github
- Docker
- Tableau Public
- Excel/Google Sheets
- Powershell


### Skills Used
- Python
- SQL
- Tableau Public
- AWS RDS
- AWS EC2
- Cron
- Bash
- Git

### Additional Resources
- [SoCo Data](https://data.sonomacounty.ca.gov/)
