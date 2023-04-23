import streamlit as st
import model as m
import pandas as pd
#import snowflake_ingestion as si
import sqlite3

st.title("Flight Delay Prediction")
st.subheader("By Group_6 DSCI6007-1")
values = []
with st.form(key='main_form',clear_on_submit=True):
    # 1,2 - Getting the Month, Day Values
    date= st.date_input("Enter the Date")
    month = date.month
    day = date.day
    # values.append(int(month))
    # values.append(int(day))

    # 3- Getting the Sheduled Deaparture
    time_sd = st.time_input('Sheduled Deaprture')
    hour_sd= str(time_sd.hour)
    minutes_sd = str(time_sd.minute)
    if len(minutes_sd)<2:
        minutes_sd = '0'+minutes_sd
    # values.append(int(hour_sd+minutes_sd))


    #4 - Deaprture_delay
    st.info('Enter -ve number for Early departure in minutes', icon="ℹ️")
    departure_delay = st.number_input("Enter Delay in Minutes",min_value = -60,max_value = 1380)
    # values.append(departure_delay)

    #5- Sheduled_arrival
    time_sa = st.time_input('Sheduled Arrival')
    hour_sa= str(time_sa.hour)
    minutes_sa = str(time_sa.minute)
    if len(minutes_sa)<2:
        minutes_sa = '0'+minutes_sa
    # values.append(int(hour_sa+minutes_sa))

    #6- Diverted
    diverted_option = st.selectbox("Was the Flight Diverted"
                ,("Yes","No"))
    # if diverted_option == "Yes":
    #     values.append(1)
    # elif diverted_option == "No":
    #     values.append(0)
    
    #7- Cancelled
    cancel_option = st.selectbox("Was the Flight Cancelled"
                ,("Yes","No"))
    # if cancel_option == "Yes":
    #     values.append(1)
    # elif cancel_option == "No":
    #     values.append(0)
    
    #8- Airsystem Delay
    airsystem_delay = st.number_input("Enter Airsystem Delay in Minutes",min_value = 0,max_value = 500)
    # values.append(airsystem_delay)  


    #9- SECURITY_DELAY
    security_delay = st.number_input("Enter Security Delay in Minutes",min_value = 0,max_value = 200)
    # values.append(security_delay)

    #10 -Airline Delay
    airline_delay = st.number_input("Enter Airline Delay in Minutes",min_value = 0,max_value = 1380)
    # values.append(airline_delay)

    #11 -late_aircraft delay
    late_aircraft_delay = st.number_input("Enter Aircraft Delay(At Previous airport) in Minutes",min_value = 0,max_value = 1380)
    # values.append(late_aircraft_delay)

    #12 - weather Delay
    weather_delay = st.number_input("Enter Security Delay in Minutes",min_value = 0,max_value = 500)
    # values.append(weather_delay)

    submit_button = st.form_submit_button(label='Submit')

if submit_button:

    values.append(int(month))
    values.append(int(day))
    values.append(int(hour_sd+minutes_sd))
    values.append(departure_delay)
    values.append(int(hour_sa+minutes_sa))    
    if diverted_option == "Yes":
        values.append(1)
    elif diverted_option == "No":
        values.append(0)
    if cancel_option == "Yes":
        values.append(1)
    elif cancel_option == "No":
        values.append(0)
    values.append(airsystem_delay)  
    values.append(security_delay)
    values.append(airline_delay)
    values.append(late_aircraft_delay)
    values.append(weather_delay)
    input = pd.DataFrame(columns = ['MONTH', 'DAY', 'SCHEDULED_DEPARTURE', 'DEPARTURE_DELAY',
       'SCHEDULED_ARRIVAL', 'DIVERTED', 'CANCELLED', 'AIR_SYSTEM_DELAY',
       'SECURITY_DELAY', 'AIRLINE_DELAY', 'LATE_AIRCRAFT_DELAY',
       'WEATHER_DELAY'])
    input.loc[0] = values
    st.header("The Flight Data You entered")
    
    input.to_csv('input.csv',index=False)
    st.dataframe(input)
predict = st.button("Predict Flight Delay Status")
if predict:
    
    new_input = pd.read_csv('input.csv')
    prediction = m.model_prediction(new_input)
    new_input['result'] = prediction
    new_input.to_csv('input.csv',index=False)
    if prediction == 1:
        st.write("Unfortunatley Flight will be Delayed")
    elif prediction == 0:
        st.write("Flight will be on time")
insert = st.button("Insert into DB")
if insert:
    
    with st.spinner("Connecting and Inserting Data to SQlite"):
        #db.insert_data()
       # insert_to_db(month, day, scheduled_departure, departure_delay, scheduled_arrival, diverted, cancelled, air_system_delay, security_delay, airline_delay, late_aircraft_delay, weather_delay, result)
     def insert_to_db(month, day, scheduled_departure, departure_delay, scheduled_arrival, diverted, cancelled, air_system_delay, security_delay, airline_delay, late_aircraft_delay, weather_delay, result):
      conn = sqlite3.connect('flight.db')
      query = "INSERT INTO user_data(MONTH, DAY, SCHEDULED_DEPARTURE, DEPARTURE_DELAY, SCHEDULED_ARRIVAL, DIVERTED, CANCELLED, AIR_SYSTEM_DELAY, SECURITY_DELAY, AIRLINE_DELAY, LATE_AIRCRAFT_DELAY, WEATHER_DELAY, result) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
      values = (month, day, scheduled_departure, departure_delay, scheduled_arrival, diverted, cancelled, air_system_delay, security_delay, airline_delay, late_aircraft_delay, weather_delay, result)
      conn.execute(query, values)
      conn.commit()
      conn.close()

    st.write("Data Instertion Complete")

# insert = st.button("Add into Database")
