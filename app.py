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

        if response.status_code == 200:
            # Parse the JSON response
            property_data = json.loads(response.text)  # Convert string to list
            return property_data[0]  # Return the first (and only) property
        else:
            st.error(f"Error fetching data: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {str(e)}")
        return None

def generate_investment_report(data):
    """Generates a detailed investment report from the property data."""
    if not data:
        st.error("No valid data available to generate the report.")
        return

    st.subheader("--- Property Smart Investment Report ---")
    st.write(f"**Address:** {data.get('formattedAddress', 'N/A')}")
    st.write(f"**Property Type:** {data.get('propertyType', 'N/A')}")
    st.write(f"**Bedrooms:** {data.get('bedrooms', 'N/A')}")
    st.write(f"**Bathrooms:** {data.get('bathrooms', 'N/A')}")
    st.write(f"**Square Footage:** {data.get('squareFootage', 'N/A')} sq ft")
    st.write(f"**Estimated Sale Price:** ${data.get('lastSalePrice', 'N/A')}")
    st.write(f"**Lot Size:** {data.get('lotSize', 'N/A')} sq ft")
    st.write(f"**Year Built:** {data.get('yearBuilt', 'N/A')}")

    # Display additional features
    features = data.get('features', {})
    st.write("**Property Features:**")
    st.write(f"- Cooling: {'Yes' if features.get('cooling', False) else 'No'}")
    st.write(f"- Heating: {'Yes' if features.get('heating', False) else 'No'}")
    st.write(f"- Pool: {'Yes' if features.get('pool', False) else 'No'}")
    st.write(f"- Garage: {'Yes' if features.get('garage', False) else 'No'}")
    st.write(f"- Architecture Type: {features.get('architectureType', 'N/A')}")
    
    # Display tax assessments and property taxes
    st.write("\n**--- Tax Assessment History ---**")
    tax_assessment = data.get('taxAssessment', {})
    for year, values in tax_assessment.items():
        st.write(f"- {year}: Total Value: ${values['value']} (Land: ${values['land']}, Improvements: ${values['improvements']})")
    
    st.write("\n**--- Property Taxes ---**")
    property_taxes = data.get('propertyTaxes', {})
    for year, values in property_taxes.items():
        st.write(f"- {year}: Total Tax: ${values['total']}")

    # Owner information
    owner_info = data.get('owner', {})
    st.write("\n**--- Owner Information ---**")
    st.write(f"- Owner Name: {', '.join(owner_info.get('names', []))}")
    st.write(f"- Mailing Address: {owner_info.get('mailingAddress', {}).get('formattedAddress', 'N/A')}")

def main():
    st.title("Property Smart Investment Report Generator")

    # Input for RapidAPI key
    rapidapi_key = st.text_input("Enter RapidAPI Key:", type="password")

    # Input for property address
    property_address = st.text_input("Enter Property Address (e.g., '5500 Grand Lake Dr, San Antonio, TX, 78244'):")

    # Input for property details
    property_type = st.selectbox("Select Property Type:", ["Single Family", "Multi Family", "Condo", "Townhouse"])
    bedrooms = st.number_input("Number of Bedrooms:", min_value=1, value=4)
    bathrooms = st.number_input("Number of Bathrooms:", min_value=1, value=2)
    square_footage = st.number_input("Square Footage:", min_value=500, value=1600)
    comp_count = st.number_input("Number of Comparable Properties:", min_value=1, value=5)

    # Button to fetch property details via API
    if st.button("Generate Investment Report"):
        if rapidapi_key and property_address:
            st.info("Fetching property details...")
            property_data = fetch_property_price_report(property_address, property_type, bedrooms, bathrooms, square_footage, comp_count, rapidapi_key)
            generate_investment_report(property_data)
        else:
            st.error("Please enter both the API key and the property address.")

if __name__ == "__main__":
    main()
