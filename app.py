import streamlit as st
import requests
import json

# Function to display property details in the Streamlit app
def display_property_details(property_data):
    """Displays property details in the Streamlit app."""
    st.subheader("Property Details:")
    
    # Ensure the property_data is in a list format
    if isinstance(property_data, list):
        if len(property_data) == 0:
            st.warning("No property details available.")
            return
        for idx, data in enumerate(property_data):
            st.write(f"### Property {idx + 1}")
            for key, value in data.items():
                # Format nested dictionaries and lists appropriately
                if isinstance(value, dict):
                    st.write(f"**{key}:**")
                    for sub_key, sub_value in value.items():
                        st.write(f"- **{sub_key}:** {sub_value}")
                elif isinstance(value, list):
                    st.write(f"**{key}:**")
                    for item in value:
                        st.write(f"- {item}")
                else:
                    st.write(f"**{key}:** {value}")
            
            # Show property images if available
            if 'media' in data and len(data['media']) > 0:
                st.image(data['media'][0]['url'], caption='Property Image', use_column_width=True)

            st.markdown("---")  # Divider between properties
    else:
        st.error("Invalid property data received.")

# Function to fetch property details using the Realty Mole API via RapidAPI
def fetch_property_info(api_key, address):
    """Fetches detailed property information using RapidAPI's Realty Mole API."""
    url = "https://realty-mole-property-api.p.rapidapi.com/properties"
    querystring = {"address": address}

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "realty-mole-property-api.p.rapidapi.com",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "x-rapidapi-ua": "RapidAPI-Playground"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            # Parse the response JSON
            properties = response.json()
            return properties
        else:
            st.error(f"Error fetching property details: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {str(e)}")
        return None

# Main function to run the Streamlit app
def main():
    st.title("🏡 Comprehensive Property Information App")
    
    # Introduction to the app
    st.write("Welcome to the Comprehensive Property Information App. "
             "Enter your RapidAPI key and the property address below to retrieve detailed property information.")
    
    # Input for RapidAPI key
    rapidapi_key = st.text_input("Enter RapidAPI Key:", type="password")

    # Input fields for property search criteria
    city = st.text_input("City:")
    state = st.text_input("State (e.g., 'TX'):")
    zip_code = st.text_input("Zip Code (optional):")
    property_type = st.selectbox("Property Type:", ["Any", "Single Family", "Condo", "Townhouse", "Multi Family", "Land", "Commercial"])

    # Input for property address
    property_address = st.text_input("Enter Property Address (e.g., '5500 Grand Lake Dr, San Antonio, TX, 78244'):")

    # Button to fetch property details via API
    if st.button("Fetch Property Data"):
        if rapidapi_key and (property_address or (city and state)):
            st.info("Fetching property details...")
            # Build the search query
            address = property_address if property_address else f"{city}, {state}, {zip_code}"
            api_result = fetch_property_info(rapidapi_key, address)
            if api_result:
                # Display the fetched property details
                display_property_details(api_result)
            else:
                st.error("Failed to retrieve property data. Please check the API key and address.")
        else:
            st.error("Please enter the API key and either the property address or city and state.")

if __name__ == "__main__":
    main()
