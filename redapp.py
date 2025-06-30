import pandas as pd
import numpy as np
import streamlit as st
from sqlalchemy import create_engine
from streamlit_option_menu import option_menu

# Create SQLAlchemy engine
engine = create_engine('postgresql://postgres:V%40risu18@localhost:5432/red_bus')

# Load data from PostgreSQL
query = "SELECT * FROM bus"
data = pd.read_sql(query, engine)

# Convert necessary columns to numeric
data['Price'] = pd.to_numeric(data['Price'], errors='coerce')
data['Seat_Availability'] = pd.to_numeric(data['Seat_Availability'], errors='coerce')
data['Star_Rating'] = pd.to_numeric(data['Star_Rating'], errors='coerce')

# FROM and TO already in DB — no extraction needed

# Streamlit UI setup
st.set_page_config(
    page_title="Redbus",
    page_icon=":redbus:",
    layout="wide",
    initial_sidebar_state="auto"
)

# Sidebar styling
st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #FFFFFF;
        margin-right: 20px;
        border-right: 2px solid #F0F0F0
    }
</style>
""", unsafe_allow_html=True)

# App Title
st.title(":red[RED BUS]")
st.header("Best online ticket booking app")
st.text("EASY TO BOOK TICKET AND EASY TO TRAVEL AND HASSEL FREE JOURNEY")

# Sidebar Navigation
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=['Home', 'Search_Bus'],
        icons=['house-door-fill', 'search'],
        menu_icon='truck-front-fill',
        default_index=0,
        styles={
            "container": {'padding': '5!important', 'background-color': '#FAF9F6'},
            "icon": {'color': "#000000", "font-size": "23px"},
            "nav-link": {'font-size': '16px', 'text-align': 'left', 'margin': '0px', '--hover-color': '#EDEADE', 'font-weight': 'bold'},
            "nav-link-selector": {'background-color': '#E6E6FA', 'font-weight': 'bold'}
        }
    )

# Home Page
if selected == 'Home':
    st.subheader("India's No 1 online Bus Booking site ")
    st.markdown("""
    redBus is India's largest brand for online bus ticket booking and offers an easy-to-use online bus experience. 
    With over 36 million satisfied customers, 3500+ bus operators to choose from, and plenty of offers on bus ticket booking, 
    redBus makes road journeys super convenient. Book buses like AC/non-AC, Sleeper, Volvo, Multi-axle, and more.
    """)
    st.image("https://newsroompost.com/wp-content/uploads/2020/05/redb.jpg", use_column_width=True)

# Search Bus Page
if selected == "Search_Bus":
    # Filters
    bustype_filter = st.multiselect('Select Bus Type:', options=data['Bus_Type'].dropna().unique()) if 'Bus_Type' in data.columns else []
    from_filter = st.multiselect('Select FROM:', options=data['FROM'].dropna().unique()) if 'FROM' in data.columns else []
    to_filter = st.multiselect('Select TO:', options=data['TO'].dropna().unique()) if 'TO' in data.columns else []

    # Fixed Price Range here
    price = st.slider('Select Price Range:', min_value=95, max_value=3000, value=(95, 3000), format="₹%d")

    star_filter = st.slider(
        'Select Star Rating Range:',
        min_value=float(data['Star_Rating'].min()),
        max_value=float(data['Star_Rating'].max()),
        value=(float(data['Star_Rating'].min()), float(data['Star_Rating'].max()))
    )

    availability = st.slider(
        'Select Seat Availability Range:',
        min_value=int(data['Seat_Availability'].min()),
        max_value=int(data['Seat_Availability'].max()),
        value=(int(data['Seat_Availability'].min()), int(data['Seat_Availability'].max()))
    )

    # Apply filters
    filter_data = data.copy()

    if bustype_filter:
        filter_data = filter_data[filter_data['Bus_Type'].isin(bustype_filter)]

    if from_filter:
        filter_data = filter_data[filter_data['FROM'].isin(from_filter)]

    if to_filter:
        filter_data = filter_data[filter_data['TO'].isin(to_filter)]

    filter_data = filter_data[(filter_data['Price'] >= price[0]) & (filter_data['Price'] <= price[1])]
    filter_data = filter_data[(filter_data['Star_Rating'] >= star_filter[0]) & (filter_data['Star_Rating'] <= star_filter[1])]
    filter_data = filter_data[(filter_data['Seat_Availability'] >= availability[0]) & (filter_data['Seat_Availability'] <= availability[1])]

    # Show results
    st.subheader("Filtered Data:")
    st.dataframe(filter_data)

    if not filter_data.empty:
        st.download_button(
            label="Download Filtered Data",
            data=filter_data.to_csv(index=False),
            file_name="filter_data.csv",
            mime="text/csv"
        )
    else:
        st.warning("No data available with the selected filters.")