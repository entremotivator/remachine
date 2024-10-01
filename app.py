import streamlit as st
import pandas as pd
import requests

def display_property_details(property_data, property_index):
    st.subheader(f"Property {property_index + 1} Details:")
    for key, value in property_data.items():
        st.write(f"{key}: {value}")

def save_property_details(properties, property_data):
    properties.append(property_data)

def fetch_property_info(api_key, address):
    url = f"https://api.realtymole.com/property?address={address}"
    headers = {"Api-Key": api_key}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching property details: {response.text}")
        return None

def main():
    st.title("Property Information App")

    # Allow user to input Realty Mole API key
    realty_mole_api_key = st.text_input("Enter Realty Mole API Key:")

    # Allow user to input address to fetch property details
    property_address = st.text_input("Enter Property Address:")

    # List to store uploaded property details
    uploaded_properties = []

    # Button to fetch property details via API
    if st.button("Fetch Property Info"):
        if realty_mole_api_key and property_address:
            st.info("Fetching property details...")
            api_result = fetch_property_info(realty_mole_api_key, property_address)
            if api_result:
                # Save and display the fetched property
                save_property_details(uploaded_properties, api_result)
                display_property_details(api_result, len(uploaded_properties))

    # Manual property input for additional details
    st.sidebar.subheader("Enter Additional Property Details:")
    property_details = {}
    for field in ["Address Line 1", "City", "State", "Zip Code", "Bedrooms", "Bathrooms",
                  "Square Footage", "Year Built", "Lot Size", "Property Type", "Last Sale Date",
                  "Value", "Land", "Cooling", "Cooling Type", "Garage", "Garage Type",
                  "Heating", "Heating Type", "Pool", "Room Count", "Roof Type"]:
        property_details[field] = st.sidebar.text_input(field)

    # Save manually entered property
    if st.sidebar.button("Save Manual Property"):
        save_property_details(uploaded_properties, property_details)
        st.sidebar.success("Property saved.")

    # Display 10 demo properties
    demo_properties = [
        {
            "Address Line 1": "123 Main St",
            "City": "Cityville",
            "State": "CA",
            "Zip Code": "12345",
            "Bedrooms": 4,
            "Bathrooms": 2.5,
            "Square Footage": 2500,
            "Year Built": 2000,
            "Last Sale Date": "2022-01-01",
            "Value": 350000,
            "Land": 50000,
            "Cooling": True,
            "Cooling Type": "Central",
            "Garage": True,
            "Garage Type": "Attached",
            "Heating": True,
            "Heating Type": "Forced Air",
            "Pool": False,
            "Room Count": 8,
            "Roof Type": "Shingle",
        },
        {
            "Address Line 1": "456 Oak St",
            "City": "Townsville",
            "State": "NY",
            "Zip Code": "67890",
            "Bedrooms": 3,
            "Bathrooms": 2,
            "Square Footage": 1800,
            "Lot Size": 6000,
            "Year Built": 1995,
            "Last Sale Date": "2022-02-15",
            "Value": 280000,
            "Land": 40000,
            "Cooling": True,
            "Cooling Type": "Central",
            "Garage": True,
            "Garage Type": "Detached",
            "Heating": True,
            "Heating Type": "Radiant",
            "Pool": True,
            "Room Count": 6,
            "Roof Type": "Tile",
        },
        # Add more demo properties here
    ]

    for i, demo_property in enumerate(demo_properties):
        st.markdown("---")
        display_property_details(demo_property, i + len(uploaded_properties))

    # Display all saved properties
    if uploaded_properties:
        st.markdown("## All Saved Properties:")
        for i, property_data in enumerate(uploaded_properties):
            st.markdown("---")
            display_property_details(property_data, i + len(demo_properties))

if __name__ == "__main__":
    main()
