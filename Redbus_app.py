import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
import pymysql

#Initializing session state for selected filter
if 'selected_star' not in st.session_state:
    st.session_state.selected_star = 'Anything'

#To connect database using SQLAlchemy 
engine = create_engine('mysql+pymysql://root:root@127.0.0.1:3306/redbus_data')

#To fetch data from database
query = "SELECT * FROM bus_routes"
data = pd.read_sql(query,engine)

#App layout
st.title('Redbus data filtering and Analysis for KSTRC')

#Adding filters

route_filter = st.multiselect('Select busroute:', options=data['route_name'].unique())

bustype_filter = st.multiselect('Select bustype:', options=data['bustype'].unique())

price_filter = st.slider('Select price range:',min_value=int(data['price'].min()),max_value=int(data['price'].max()),value=(int(data['price'].min()),int(data['price'].max())))

star_filter = st.slider('Select star range:', min_value=int(data['star_rating'].min()), max_value=int(data['star_rating'].max()),value=(int(data['star_rating'].min()),int(data['star_rating'].max())))


availability_filter = st.slider('Select Seat Availability Range:', min_value=int(data['seats_available'].min()), max_value=int(data['seats_available'].max()), value=(int(data['seats_available'].min()), int(data['seats_available'].max())))


#Filtering data based on the user input
filtered_data = data

if bustype_filter:
    filtered_data = filtered_data[filtered_data['bustype'].isin(bustype_filter)]

if route_filter:
    filtered_data = filtered_data[filtered_data['route_name'].isin(route_filter)]

filtered_data = filtered_data[(filtered_data['price'] >= price_filter[0]) & (filtered_data['price'] <= price_filter[1])]

filtered_data = filtered_data[(filtered_data['star_rating'] >= star_filter[0]) & (filtered_data['star_rating'] <= star_filter[1])]

filtered_data = filtered_data[(filtered_data['seats_available'] >= availability_filter[0]) & (filtered_data['seats_available'] <= availability_filter[1])]

#To display filtered data
st.write('Filtered Datas:')
st.dataframe(filtered_data)

#Adding download button to export the filtered data

if not filtered_data.empty:
    st.download_button(
            label="Download",
            data=filtered_data.to_csv(index=False),
            file_name="filtered_data.csv",
            mime="text/csv"

    )

else:
    st.warning("No data available with the selected filters.")