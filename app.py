import streamlit as st
import requests

# Function to fetch ZPID from the address using Zillow API (assumed endpoint)
def fetch_zpid(api_key, address):
    url = "https://zillow-zestimate.p.rapidapi.com/zestimate"
    
    querystring = {"address": address}
    
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "zillow-zestimate.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        return response.json().get("zpid", None)  # Return ZPID if request is successful
    else:
        st.error("Error fetching ZPID from API. Status Code: {}".format(response.status_code))
        return None

# Function to fetch property details from Zillow API using ZPID
def fetch_property_data(api_key, zpid):
    url = "https://zillow-zestimate.p.rapidapi.com/zestimate"
    
    querystring = {"zpid": zpid}
    
    headers = {
        "x-rapidapi-key": api_key,  # User's API key
        "x-rapidapi-host": "zillow-zestimate.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        return response.json()  # Return JSON data if request is successful
    else:
        st.error("Error fetching data from API. Status Code: {}".format(response.status_code))
        return None

# Streamlit application layout
st.title("Zillow Property Finder")

# Input for user's API key
api_key = st.text_input("Enter your Zillow API Key:", type="password")

# Input for Property Address
address = st.text_input("Enter the Property Address:")

# Button to fetch property details
if st.button("Get Property Details"):
    if api_key and address:
        # Fetch ZPID using the address
        zpid = fetch_zpid(api_key, address)
        
        if zpid:
            # Fetch property details using ZPID
            property_data = fetch_property_data(api_key, zpid)
            
            if property_data:
                # Display property details
                st.subheader("Property Details")
                st.write("**ZPID:**", property_data.get("zpid", "N/A"))
                st.write("**Home Type:**", property_data.get("homeType", "N/A"))
                st.write("**Price Estimate:**", property_data.get("amount", "N/A"))
                st.write("**Last Updated:**", property_data.get("lastUpdated", "N/A"))
                
                # Display formatted address
                formatted_address = property_data.get("address", {}).get("formatted", "N/A")
                st.write("**Address:**", formatted_address)

                # Display additional information if available
                if "valueChange" in property_data:
                    st.write("**Value Change:**", property_data["valueChange"], "from last month")

                # Display images if available
                images = property_data.get("images", [])
                if images:
                    st.image(images, caption="Property Images", use_column_width=True)
                else:
                    st.write("No images available.")
            else:
                st.warning("No data found for the given address.")
        else:
            st.warning("No ZPID found for the given address.")
    else:
        st.error("Please enter your API key and a valid property address.")

# Run the Streamlit app
if __name__ == "__main__":
    st.run()

