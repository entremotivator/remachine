import streamlit as st
import requests

# Function to fetch property details from API
def fetch_property_data(address):
    # Replace this URL with your actual API endpoint
    api_url = "https://api.example.com/properties"  # Example API endpoint
    params = {'address': address}  # Address parameter
    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        return response.json()  # Return JSON data if request is successful
    else:
        st.error("Error fetching data from API.")
        return None

# Streamlit application layout
st.title("Real Estate Property Finder")

# Input for property address
address = st.text_input("Enter the property address:", "6937 Nansen St, Flushing, NY 11375")

# Button to fetch property details
if st.button("Get Property Details"):
    property_data = fetch_property_data(address)
    
    if property_data:
        # Display property details
        st.subheader("Property Details")
        
        # Display relevant property data
        st.write("**Address:**", property_data.get("fullValue", "N/A"))
        st.write("**Price:**", property_data.get("price", "N/A"))
        st.write("**Bedrooms:**", property_data.get("bedrooms", "N/A"))
        st.write("**Bathrooms:**", property_data.get("bathrooms", "N/A"))
        st.write("**Living Area:**", property_data.get("livingArea", "N/A"), "sqft")
        st.write("**Lot Size:**", property_data.get("lotSize", "N/A"), "sqft")
        st.write("**Description:**", property_data.get("description", "N/A"))
        
        # Display property images
        images = property_data.get("images", [])
        if images:
            st.image(images, caption="Property Images", use_column_width=True)
        else:
            st.write("No images available.")
        
        # Display agent information
        st.subheader("Agent Information")
        st.write("**Agent Name:**", property_data.get("agentName", "N/A"))
        st.write("**Agent Phone:**", property_data.get("agentPhoneNumber", "N/A"))
        st.write("**Broker Name:**", property_data.get("brokerName", "N/A"))
        
        # Add any other relevant property details you want to display

# Run the Streamlit app
if __name__ == "__main__":
    st.run()
