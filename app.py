import streamlit as st
import requests
import pandas as pd

# Function to display property details in the Streamlit app
def display_property_details(property_data):
    """Displays property details in the Streamlit app."""
    st.subheader("Property Details:")
    for key, value in property_data.items():
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

# Function to export property data to CSV
def export_to_csv(property_data):
    """Exports the property data to a CSV file."""
    df = pd.DataFrame(property_data)
    csv = df.to_csv(index=False)
    return csv

# Main function to run the Streamlit app
def main():
    st.title("Comprehensive Property Information App")

    # Input for RapidAPI key
    rapidapi_key = st.text_input("Enter RapidAPI Key:", type="password")

    # Input for property address (e.g., '5500 Grand Lake Dr, San Antonio, TX, 78244')
    property_address = st.text_input("Enter Property Address (e.g., '5500 Grand Lake Dr, San Antonio, TX, 78244'):")

    # Button to fetch property details via API
    if st.button("Fetch Property Data"):
        if rapidapi_key and property_address:
            st.info("Fetching property details...")
            api_result = fetch_property_info(rapidapi_key, property_address)
            if api_result:
                # Display the fetched property details
                if isinstance(api_result, list) and len(api_result) > 0:
                    for property_data in api_result:
                        display_property_details(property_data)

                    # Button to export property data
                    if st.button("Export Property Data to CSV"):
                        csv = export_to_csv(api_result)
                        st.download_button(
                            label="Download CSV",
                            data=csv,
                            file_name="property_data.csv",
                            mime="text/csv"
                        )
                else:
                    st.error("No property details found for the provided address.")
        else:
            st.error("Please enter both the API key and the property address.")

if __name__ == "__main__":
    main()
