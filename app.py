import streamlit as st
import http.client
import json

# Function to display all property details in the Streamlit app
def display_property_details(property_data):
    st.subheader("Property Details:")
    for key, value in property_data.items():
        st.write(f"{key}: {value}")

# Function to fetch property details using the Realty Mole API via RapidAPI and http.client
def fetch_property_info(api_key, address):
    """Fetches detailed property information using RapidAPI's Realty Mole API."""
    conn = http.client.HTTPSConnection("realty-mole-property-api.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': "realty-mole-property-api.p.rapidapi.com"
    }

    url = f"/properties?address={address}"
    try:
        conn.request("GET", url, headers=headers)
        res = conn.getresponse()
        data = res.read()
        conn.close()

        if res.status == 200:
            return json.loads(data.decode("utf-8"))
        else:
            st.error(f"Error fetching property details: {res.status} - {res.reason}")
            return None
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        return None

# Main function to run the Streamlit app
def main():
    st.title("Comprehensive Property Information App")

    # Input for RapidAPI key
    rapidapi_key = st.text_input("Enter RapidAPI Key:")

    # Input for property address (e.g., '5500 Grand Lake Dr, San Antonio, TX, 78244')
    property_address = st.text_input("Enter Property Address (e.g., '5500 Grand Lake Dr, San Antonio, TX, 78244'):")

    # Button to fetch property details via API
    if st.button("Fetch Property Data"):
        if rapidapi_key and property_address:
            st.info("Fetching property details...")
            formatted_address = property_address.replace(" ", "%20")  # Format the address for the API
            api_result = fetch_property_info(rapidapi_key, formatted_address)
            if api_result:
                # Display the fetched property details
                if isinstance(api_result, dict):
                    display_property_details(api_result)
                else:
                    st.error("No property details found for the provided address.")
        else:
            st.error("Please enter both the API key and the property address.")

if __name__ == "__main__":
    main()

