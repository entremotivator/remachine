import streamlit as st
import requests

def display_property_details(property_data, property_index):
    """Displays the details of a property."""
    st.subheader(f"Property {property_index + 1} Details:")
    for key, value in property_data.items():
        st.write(f"{key}: {value}")

def save_property_details(properties, property_data):
    """Saves the fetched property details into a list."""
    properties.append(property_data)

def fetch_property_info(api_key, address):
    """Fetches property details from the Realty Mole API."""
    url = f"https://api.realtymole.com/property?address={address}"
    headers = {"Api-Key": api_key}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching property details: {response.text}")
        return None

def main():
    """Main function for the Streamlit app."""
    st.title("Property Information App")

    # Allow user to input Realty Mole API key
    realty_mole_api_key = st.text_input("Enter Realty Mole API Key:")
    
    # Allow user to input the property address to search
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
                display_property_details(api_result, len(uploaded_properties) - 1)  # Use len(uploaded_properties)-1 for correct index
        else:
            st.error("Please enter both API key and property address.")

    # Display all fetched properties
    if uploaded_properties:
        st.write("All Fetched Properties:")
        for i, property_data in enumerate(uploaded_properties):
            display_property_details(property_data, i)

if __name__ == "__main__":
    main()
