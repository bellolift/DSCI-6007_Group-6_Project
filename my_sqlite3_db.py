import streamlit as st
import sqlite3
import pandas as pd
import joblib

# Load the prediction model
model = joblib.load('finalized_model.sav')

#create a function to connect to the database and insert data
def insert_to_db(month, day, scheduled_departure, departure_delay, scheduled_arrival, diverted, cancelled, air_system_delay, security_delay, airline_delay, late_aircraft_delay, weather_delay, result):
    conn = sqlite3.connect('flight.db')
    query = "INSERT INTO user_data(MONTH, DAY, SCHEDULED_DEPARTURE, DEPARTURE_DELAY, SCHEDULED_ARRIVAL, DIVERTED, CANCELLED, AIR_SYSTEM_DELAY, SECURITY_DELAY, AIRLINE_DELAY, LATE_AIRCRAFT_DELAY, WEATHER_DELAY, result) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    values = (month, day, scheduled_departure, departure_delay, scheduled_arrival, diverted, cancelled, air_system_delay, security_delay, airline_delay, late_aircraft_delay, weather_delay, result)
    conn.execute(query, values)
    conn.commit()
    conn.close()


# Connect to the SQLite database
conn = sqlite3.connect('flights.db')
c = conn.cursor()

# Define the SQL query to insert the user data into the database
insert_query = "INSERT INTO user_data (MONTH, DAY, SCHEDULED_DEPARTURE, DEPARTURE_DELAY, SCHEDULED_ARRIVAL, DIVERTED, CANCELLED, AIR_SYSTEM_DELAY, SECURITY_DELAY, AIRLINE_DELAY, LATE_AIRCRAFT_DELAY, WEATHER_DELAY, result) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

# Define a function to execute the SQL query with user input
def predict_and_insert(month, day, scheduled_departure, departure_delay, scheduled_arrival, diverted, cancelled, air_system_delay, security_delay, airline_delay, late_aircraft_delay, weather_delay):
    # Make the prediction using the model
    prediction = model.predict([[month, day, scheduled_departure, departure_delay, scheduled_arrival, diverted, cancelled, air_system_delay, security_delay, airline_delay, late_aircraft_delay, weather_delay]])[0]
    
    # Insert the user data and prediction result into the database
    c.execute(insert_query, (month, day, scheduled_departure, departure_delay, scheduled_arrival, diverted, cancelled, air_system_delay, security_delay, airline_delay, late_aircraft_delay, weather_delay, prediction))
    conn.commit()
    
    return prediction