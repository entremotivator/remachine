import streamlit as st
import requests

# Function to display all property details in the Streamlit app
def display_property_details(property_data):
    """Displays property details in the Streamlit app."""
    st.subheader("Property Details:")
    details = {
        "Address Line 1": property_data.get("addressLine1", "N/A"),
        "City": property_data.get("city", "N/A"),
        "State": property_data.get("state", "N/A"),
        "Zip Code": property_data.get("zipCode", "N/A"),
        "Formatted Address": property_data.get("formattedAddress", "N/A"),
        "Assessor ID": property_data.get("assessorID", "N/A"),
        "Bedrooms": property_data.get("bedrooms", "N/A"),
        "County": property_data.get("county", "N/A"),
        "Legal Description": property_data.get("legalDescription", "N/A"),
        "Square Footage": property_data.get("squareFootage", "N/A"),
        "Subdivision": property_data.get("subdivision", "N/A"),
        "Year Built": property_data.get("yearBuilt", "N/A"),
        "Bathrooms": property_data.get("bathrooms", "N/A"),
        "Lot Size": property_data.get("lotSize", "N/A"),
        "Property Type": property_data.get("propertyType", "N/A"),
        "Last Sale Date": property_data.get("lastSaleDate", "N/A"),
        "Architecture Type": property_data.get("architectureType", "N/A"),
        "Cooling": property_data.get("cooling", "N/A"),
        "Cooling Type": property_data.get("coolingType", "N/A"),
        "Exterior Type": property_data.get("exteriorType", "N/A"),
        "Floor Count": property_data.get("floorCount", "N/A"),
        "Foundation Type": property_data.get("foundationType", "N/A"),
        "Garage": property_data.get("garage", "N/A"),
        "Garage Type": property_data.get("garageType", "N/A"),
        "Heating": property_data.get("heating", "N/A"),
        "Heating Type": property_data.get("heatingType", "N/A"),
        "Pool": property_data.get("pool", "N/A"),
        "Roof Type": property_data.get("roofType", "N/A"),
        "Room Count": property_data.get("roomCount", "N/A"),
        "Unit Count": property_data.get("unitCount", "N/A"),
        "Location": f"Latitude: {property_data.get('latitude', 'N/A')}, Longitude: {property_data.get('longitude', 'N/A')}"
    }

    # Displaying values in a clean format
    for key, value in details.items():
        st.write(f"**{key}:** {value}")

    # Displaying values related to property valuation
    if 'value' in property_data:
        st.subheader("Property Valuations:")
        for i in range(0, len(property_data['value']), 2):
            land_value = property_data['land'][i//2] if 'land' in property_data else "N/A"
            improvements_value = property_data['improvements'][i//2] if 'improvements' in property_data else "N/A"
            total_value = property_data['value'][i] if 'value' in property_data else "N/A"
            st.write(f"- Value: {total_value}, Land: {land_value}, Improvements: {improvements_value}")

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
    st.title("Comprehensive Property Information App")

    # Input for RapidAPI key
    rapidapi_key = st.text_input("Enter RapidAPI Key:")

    # Input for property address
    property_address = st.text_input("Enter Property Address (e.g., '5500 Grand Lake Dr, San Antonio, TX 78244'): ")

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
                else:
                    st.error("No property details found for the provided address.")
        else:
            st.error("Please enter both the API key and the property address.")

if __name__ == "__main__":
    main()
