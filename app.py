import streamlit as st
import pandas as pd

def display_property_details(property_data, property_index):
    st.subheader(f"Property {property_index + 1} Details:")
    for key, value in property_data.items():
        st.write(f"{key}: {value}")

def save_property_details(properties, property_data):
    properties.append(property_data)

def main():
    st.title("Property Information App")

    # Allow user to upload a file
    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])

    # List to store uploaded property details
    uploaded_properties = []

    if uploaded_file is not None:
        # Load data from the uploaded file
        df = pd.read_excel(uploaded_file, sheet_name=None)

        for sheet_name, sheet_data in df.items():
            st.markdown(f"## Sheet: {sheet_name}")

            for index, row in sheet_data.iterrows():
                st.markdown("---")
                property_details = row.to_dict()
                display_property_details(property_details, index)
                save_property_details(uploaded_properties, property_details)

    # Display all saved properties
    if uploaded_properties:
        st.markdown("## All Saved Properties:")
        for i, property_data in enumerate(uploaded_properties):
            display_property_details(property_data, i)

if __name__ == "__main__":
    main()
