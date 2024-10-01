import streamlit as st
import requests

# Function to display property listings
def display_listings(listings):
    """Displays property listings in the Streamlit app."""
    st.subheader("Property Listings:")
    if listings:
        for listing in listings:
            st.write(f"**Address:** {listing.get('address')}, {listing.get('city')}, {listing.get('state')} {listing.get('zip')}")
            st.write(f"**Price:** ${listing.get('price')}")
            st.write(f"**Type:** {listing.get('property_type')}")
            st.write(f"**Bedrooms:** {listing.get('bedrooms')}")
            st.write(f"**Bathrooms:** {listing.get('bathrooms')}")
            st.write(f"**Link:** [View Listing]({listing.get('property_url')})")
            st.write("---")
    else:
        st.write("No listings found for the provided city or zip code.")

# Function to fetch property listings using the Realty Mole API via RapidAPI
def fetch_listings(api_key, city=None, zip_code=None):
    """Fetches property listings based on city or zip code."""
    url = "https://realty-mole-property-api.p.rapidapi.com/saleListings"
    querystring = {"limit": "10"}
    
    if city:
        querystring["city"] = city
    if zip_code:
        querystring["zip"] = zip_code

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "realty-mole-property-api.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            # Parse the response JSON
            listings = response.json()
            return listings
        else:
            st.error(f"Error fetching listings: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {str(e)}")
        return None

# Main function to run the Streamlit app
def main():
    st.title("Property Listings Search App")

    # Input for RapidAPI key
    rapidapi_key = st.text_input("Enter RapidAPI Key:")

    # Inputs for city or zip code
    city = st.text_input("Enter City (e.g., Austin):")
    zip_code = st.text_input("Or Enter Zip Code (e.g., 78701):")

    # Button to fetch property listings via API
    if st.button("Search Listings"):
        if rapidapi_key and (city or zip_code):
            st.info("Fetching property listings...")
            listings_result = fetch_listings(rapidapi_key, city, zip_code)
            if listings_result:
                # Display the fetched property listings
                display_listings(listings_result)
            else:
                st.error("No property listings found.")
        else:
            st.error("Please enter your API key and at least one search parameter (city or zip code).")

if __name__ == "__main__":
    main()
