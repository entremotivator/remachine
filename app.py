import streamlit as st

def display_property_details(property_data):
    st.subheader("Property Details:")
    for key, value in property_data.items():
        st.write(f"{key}: {value}")

def display_financial_details(financial_data):
    st.subheader("Financial Details:")
    for year, details in financial_data.items():
        st.write(f"Year {year}:")
        for category, amount in details.items():
            st.write(f"{category}: {amount}")

def display_geographical_details(geographical_data):
    st.subheader("Geographical Details:")
    for key, value in geographical_data.items():
        st.write(f"{key}: {value}")

def display_additional_property_information(additional_data):
    st.subheader("Additional Property Information:")
    for index, data in additional_data.items():
        st.write(f"{index}:")
        for key, value in data.items():
            st.write(f"{key}: {value}")

def main():
    property_details = {
        "Address Line 1": "5500 Grand Lake Dr",
        "City": "San Antonio",
        "State": "TX",
        "Zip Code": "78244",
        "Formatted Address": "5500 Grand Lake Dr, San Antonio, TX 78244",
        "Assessor ID": "05076-103-0500",
        "Bedrooms": 3,
        "County": "Bexar",
        "Legal Description": "B 5076A BLK 3 LOT 50",
        "Square Footage": 1878,
        "Subdivision": "CONV A/S CODE",
        "Year Built": 1973,
        "Bathrooms": 2,
        "Lot Size": 8843,
        "Property Type": "Single Family",
        "Last Sale Date": "2017-10-19T00:00:00.000Z",
        "Architecture Type": "Contemporary",
        "Cooling": True,
        "Cooling Type": "Central",
        "Exterior Type": "Wood",
        "Floor Count": 1,
        "Foundation Type": "Slab",
        "Garage": True,
        "Garage Type": "Garage",
        "Heating": True,
        "Heating Type": "Forced Air",
        "Pool": True,
        "Roof Type": "Asphalt",
        "Room Count": 5,
        "Unit Count": 1,
    }

    financial_details = {
        "Year 1": {"Value": 126510, "Land": 18760},
        "Year 2": {"Improvements": 107750, "Value": 135430, "Land": 23450},
        "Year 3": {"Improvements": 111980, "Value": 142610, "Land": 23450},
        "Year 4": {"Improvements": 119160, "Value": 163440, "Land": 45050},
        "Year 5": {"Improvements": 118390, "Value": 197600, "Land": 49560},
        "Year 6": {"Improvements": 148040, "Total": 2997, "Total": 3468},
    }

    geographical_details = {
        "ID": "5500-Grand-Lake-Dr,-San-Antonio,-TX-78244",
        "Longitude": -98.351442,
        "Latitude": 29.475962,
    }

    additional_property_information = {
        "0": {"Owner": "MICHEAL ONEAL SMITH", "ID": "149-Weaver-Blvd,-Weaverville,-NC-28787"},
        "Address Line 1": "149 Weaver Blvd",
        "City": "Weaverville",
        "State": "NC",
        "Zip Code": "28787",
    }

    st.title("Property Information App")

    display_property_details(property_details)
    display_financial_details(financial_details)
    display_geographical_details(geographical_details)
    display_additional_property_information(additional_property_information)

if __name__ == "__main__":
    main()
