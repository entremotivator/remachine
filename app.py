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
    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

    # List to store uploaded property details
    uploaded_properties = []

    # Add multiple properties interactively
    add_properties = st.checkbox("Add Properties")
    while add_properties:
        property_details = {}
        st.sidebar.subheader("Enter Property Details:")
        for field in ["Address Line 1", "City", "State", "Zip Code", "Formatted Address",
                      "Assessor ID", "Bedrooms", "County", "Legal Description", "Square Footage",
                      "Subdivision", "Year Built", "Bathrooms", "Lot Size", "Property Type",
                      "Last Sale Date", "Architecture Type", "Cooling", "Cooling Type",
                      "Exterior Type", "Floor Count", "Foundation Type", "Garage", "Garage Type",
                      "Heating", "Heating Type", "Pool", "Roof Type", "Room Count", "Unit Count"]:
            property_details[field] = st.sidebar.text_input(field)

        st.sidebar.subheader("Enter Financial Details:")
        financial_details = {}
        for year in range(1, 7):
            year_str = f"Year {year}"
            financial_details[year_str] = {}
            financial_details[year_str]["Value"] = st.sidebar.number_input(f"{year_str} - Value", value=0)
            financial_details[year_str]["Land"] = st.sidebar.number_input(f"{year_str} - Land", value=0)

        st.sidebar.subheader("Enter Geographical Details:")
        geographical_details = {}
        geographical_details["ID"] = st.sidebar.text_input("ID")
        geographical_details["Longitude"] = st.sidebar.number_input("Longitude")
        geographical_details["Latitude"] = st.sidebar.number_input("Latitude")

        st.sidebar.subheader("Enter Additional Property Information:")
        additional_property_information = {}
        for i in range(3):  # You can adjust the number of additional entries
            key = st.sidebar.text_input(f"Additional Key {i + 1}")
            value = st.sidebar.text_input(f"Additional Value {i + 1}")
            additional_property_information[key] = value

        # Save and display the current property
        if st.sidebar.button("Save Property"):
            save_property_details(uploaded_properties, {
                "Property Details": property_details,
                "Financial Details": financial_details,
                "Geographical Details": geographical_details,
                "Additional Property Information": additional_property_information
            })

        # Add another property or finish
        add_properties = st.sidebar.checkbox("Add Another Property")

    # Display properties from the uploaded CSV
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        for index, row in df.iterrows():
            st.markdown("---")
            display_property_details(row.to_dict(), index)

    # Display 10 demo properties
    demo_properties = [
        {
            "Address Line 1": "123 Main St",
            "City": "Cityville",
            "State": "CA",
            "Zip Code": "12345",
            "Bedrooms": 4,
            "Bathrooms": 2.5,
            "Square Footage": 2500,
            "Lot Size": 8000,
            "Year Built": 2000,
            "Last Sale Date": "2022-01-01",
            "Value": 350000,
            "Land": 50000,
            "Cooling": True,
            "Cooling Type": "Central",
            "Garage": True,
            "Garage Type": "Attached",
            "Heating": True,
            "Heating Type": "Forced Air",
            "Pool": False,
            "Room Count": 8,
            "Roof Type": "Shingle",
        },
        # Add more demo properties
        {
            "Address Line 1": "456 Oak St",
            "City": "Townsville",
            "State": "NY",
            "Zip Code": "67890",
            "Bedrooms": 3,
            "Bathrooms": 2,
            "Square Footage": 1800,
            "Lot Size": 6000,
            "Year Built": 1995,
            "Last Sale Date": "2022-02-15",
            "Value": 280000,
            "Land": 40000,
            "Cooling": True,
            "Cooling Type": "Central",
            "Garage": True,
            "Garage Type": "Detached",
            "Heating": True,
            "Heating Type": "Radiant",
            "Pool": True,
            "Room Count": 6,
            "Roof Type": "Tile",
        },
        # Add more demo properties
        # ...
    ]

    for i, demo_property in enumerate(demo_properties):
        st.markdown("---")
        display_property_details(demo_property, i + len(uploaded_properties))

    # Display all saved properties
    if uploaded_properties:
        st.markdown("## All Saved Properties:")
        for i, property_data in enumerate(uploaded_properties):
            st.markdown("---")
            display_property_details(property_data["Property Details"], i + len(demo_properties))

if __name__ == "__main__":
    main()
