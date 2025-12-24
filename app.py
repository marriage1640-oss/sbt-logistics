import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import date

# Page Config
st.set_page_config(page_title="SBT Logistics Cloud", layout="wide")

st.title("🚛 SBT Logistics - Cloud Management System")

# Establish Google Sheets Connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Fetch existing data
df = conn.read(ttl="0s") # ttl=0 means it always fetches fresh data

# Sidebar Entry Form
st.sidebar.header("Add New Entry")
with st.sidebar.form(key="logistics_form"):
    entry_date = st.date_input("Date", date.today())
    location = st.selectbox("Select Location", ["Birgunj", "Butwal", "Bhairahawa"])
    truck_no = st.text_input("Truck Number")
    booking_amt = st.number_input("Booking Amount", min_value=0, step=100)
    truck_charges = st.number_input("Truck Charges", min_value=0, step=100)
    
    submit_button = st.form_submit_button(label="Save to Cloud")

if submit_button:
    if truck_no:
        # Create new row
        new_row = pd.DataFrame([{
            "Date": str(entry_date),
            "Location": location,
            "Truck Number": truck_no,
            "Booking Amount": booking_amt,
            "Truck Charges": truck_charges,
            "Gross Profit": booking_amt - truck_charges
        }])
        
        # Add to existing data
        updated_df = pd.concat([df, new_row], ignore_index=True)
        
        # Update Google Sheet
        conn.update(data=updated_df)
        st.success("Data saved successfully to Google Sheets!")
        st.rerun()
    else:
        st.error("Truck Number is required")

# Display Tabs
tab1, tab2, tab3, tab4 = st.tabs(["All Records", "Birgunj", "Butwal", "Bhairahawa"])

with tab1:
    st.dataframe(df, use_container_width=True)

with tab2:
    st.dataframe(df[df["Location"] == "Birgunj"], use_container_width=True)

with tab3:
    st.dataframe(df[df["Location"] == "Butwal"], use_container_width=True)

with tab4:
    st.dataframe(df[df["Location"] == "Bhairahawa"], use_container_width=True)

# Calculation Summary
st.divider()
if not df.empty:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Booking", f"Rs. {df['Booking Amount'].sum():,.2f}")
    col2.metric("Total Charges", f"Rs. {df['Truck Charges'].sum():,.2f}")
    col3.metric("Net Profit", f"Rs. {df['Gross Profit'].sum():,.2f}")