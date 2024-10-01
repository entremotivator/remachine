import streamlit as st
from zillow import get_zpids, fetch_property_details

# Streamlit application layout
st.title("Zillow Property Finder")

# Input for user's API key
api_key = st.text_input("Enter your Zillow API Key:", type="password")

# Input for ZIP code
zipcode = st.text_input("Enter the ZIP Code:")

# Button to fetch property details
if st.button("Get Property Details"):
    if api_key and zipcode:
        # Fetch ZPIDs using the provided ZIP code
        zpids = get_zpids(int(zipcode), sort_by='newest')
        
        if zpids:
            property_data = fetch_property_details(api_key, zpids[0])  # Get details for the first ZPID
            
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
                st.warning("No data found for the given ZIP code.")
        else:
            st.warning("No listings found for the given ZIP code.")
    else:
        st.error("Please enter your API key and a valid ZIP code.")

# Run the Streamlit app
if __name__ == "__main__":
    st.run()

