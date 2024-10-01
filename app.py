import streamlit as st
import requests

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
            return response.json()
        else:
            st.error(f"Error fetching data: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {str(e)}")
        return None

def generate_investment_report(data):
    """Generates a detailed investment report from the property data."""
    if not data or 'salePrice' not in data:
        st.error("No valid data available to generate the report.")
        return

    st.subheader("--- Property Smart Investment Report ---")
    st.write(f"**Address:** {data.get('address', 'N/A')}")
    st.write(f"**Property Type:** {data.get('propertyType', 'N/A')}")
    st.write(f"**Bedrooms:** {data.get('bedrooms', 'N/A')}")
    st.write(f"**Bathrooms:** {data.get('bathrooms', 'N/A')}")
    st.write(f"**Square Footage:** {data.get('squareFootage', 'N/A')} sq ft")
    st.write(f"**Estimated Sale Price:** ${data.get('salePrice', 'N/A')}")
    st.write(f"**Comparable Properties Count:** {data.get('compCount', 'N/A')}")

    st.write("\n**--- Comparable Properties ---**")
    if 'comps' in data:
        for comp in data['comps']:
            st.write(f"- Address: {comp.get('address', 'N/A')}, Sale Price: ${comp.get('salePrice', 'N/A')}, Bedrooms: {comp.get('bedrooms', 'N/A')}, Bathrooms: {comp.get('bathrooms', 'N/A')}, Square Footage: {comp.get('squareFootage', 'N/A')}")
    else:
        st.write("No comparable properties found.")

    st.write("\n**--- Investment Insights ---**")
    average_price = sum(comp['salePrice'] for comp in data.get('comps', []) if 'salePrice' in comp) / max(len(data.get('comps', [])), 1)
    st.write(f"**Average Sale Price of Comparable Properties:** ${average_price:.2f}")
    st.write("Consider the following before making an investment:")
    st.write("- Analyze market trends in the area.")
    st.write("- Compare the property with similar listings.")
    st.write("- Assess potential renovation costs if applicable.")
    st.write("- Calculate potential rental income and return on investment.")

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
