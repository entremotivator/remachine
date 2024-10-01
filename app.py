import streamlit as st
import requests
import json

def fetch_property_price_report(address, property_type, bedrooms, bathrooms, square_footage, comp_count, api_key):
    """Fetches the sale price report for a specified property using the Realty Mole API."""
    url = "https://realty-mole-property-api.p.rapidapi.com/salePrice"

    querystring = {
        "address": address,
        "propertyType": property_type,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "squareFootage": square_footage,
        "compCount": comp_count
    }

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "realty-mole-property-api.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)

        # Check for a successful response
        if response.status_code == 200:
            # Parse the JSON response
            property_data = response.json()  # Convert the response to a JSON object

            # Check if property_data is a non-empty list
            if property_data and isinstance(property_data, list):
                return property_data[0]  # Return the first (and only) property
            else:
                st.error("No property data found or the response is not in the expected format.")
                return None
        else:
            st.error(f"Error fetching data: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {str(e)}")
        return None
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON: {str(e)}")
        return None

def main():
    st.title("Property Smart Investment Report")
    
    # User input for property details
    rapidapi_key = st.text_input("Enter your RapidAPI Key", type="password")
    property_address = st.text_input("Enter Property Address")
    property_type = st.selectbox("Select Property Type", ["Single Family", "Condo", "Multi-Family", "Townhouse", "Land"])
    bedrooms = st.number_input("Number of Bedrooms", min_value=0, max_value=10, value=4)
    bathrooms = st.number_input("Number of Bathrooms", min_value=0, max_value=10, value=2)
    square_footage = st.number_input("Square Footage", min_value=0, max_value=10000, value=1600)
    comp_count = st.number_input("Number of Comparables", min_value=1, max_value=50, value=5)

    if st.button("Get Property Price Report"):
        # Fetch property data
        property_data = fetch_property_price_report(property_address, property_type, bedrooms, bathrooms, square_footage, comp_count, rapidapi_key)

        # Output the result
        if property_data:
            st.json(property_data)  # Pretty print the result as JSON
        else:
            st.write("No data retrieved.")

if __name__ == "__main__":
    main()
