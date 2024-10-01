import streamlit as st
import requests

# Function to display property details in the Streamlit app
def display_property_details(property_data):
    st.subheader("Property Details:")
    for key, value in property_data.items():
        st.write(f"{key}: {value}")

# Function to fetch property information using the Realty Mole API via RapidAPI
def fetch_property_info(api_key, address):
    """Fetches property details using RapidAPI's Realty Mole API."""
    url = f"https://realty-mole-property-api.p.rapidapi.com/rentalListings/{address}"

    headers = {
        "x-rapidapi-host": "realty-mole-property-api.p.rapidapi.com",
        "x-rapidapi-key": api_key
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching property details: {str(e)}")
        return None

# Main function to run the Streamlit app
def main():
    st.title("Property Rental Information App")

    # Input for RapidAPI key
    rapidapi_key = st.text_input("Enter RapidAPI Key:")

    # Input for property address (formatted for the API: e.g., '1702-Cherry-Orchard-Dr,-Austin,-TX-78745')
    property_address = st.text_input("Enter Property Address (formatted like '1702-Cherry-Orchard-Dr,-Austin,-TX-78745'):")

    # Button to fetch property details via API
    if st.button("Fetch Property Info"):
        if rapidapi_key and property_address:
            st.info("Fetching property details...")
            api_result = fetch_property_info(rapidapi_key, property_address)
            if api_result:
                # Display the fetched property details
                if isinstance(api_result, list) and len(api_result) > 0:
                    for property_data in api_result:
                        display_property_details(property_data)
                else:
                    st.error("No property details found for the provided address.")
        else:
            st.error("Please enter both the API key and the property address.")

if __name__ == "__main__":
    main()

