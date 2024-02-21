import streamlit as st
import pandas as pd
import math


def main():
    st.title("Directions to nearest AED")
    
    # Button to inform the nearest first responder
    if st.button('Inform nearest first responder'):
        # Display the message once the button is clicked
        st.write('Nearest first responder is informed and is 5 min away')
        
      # Get query parameters from the URL
    # params = st.experimental_get_query_params()
    # params1=st.query_params.to_dict()
    if "lat1" in st.query_params and st.query_params["lat1"] is not None:
        lat1_value = 51.213231907768254
    # long1_value= 4.424526343527039
    # lat1_value =st.query_params["lat1"]
    if "long1" in st.query_params and st.query_params["long1"] is not None:
        long1_value =st.query_params["long1"]
    
    
    
    newared_aed = fetch_least_distance(lat1_value,long1_value)
    # self.lat2_value =st.query_params["lat2"]
    # self.long2_value =st.query_params["long2"]
    lat2_value = newared_aed.latitude
    long2_value = newared_aed.longitude


    # Render the iframe
    st.write("<iframe ", f"src=https://www.google.com/maps/embed/v1/directions?key=AIzaSyBMON2WBju7Gd7G2UY_P60O-wNHvs6u6V4&origin={lat1_value},{long1_value}&destination={lat2_value},{long2_value}&mode=walking&avoid=tolls|highways", f"height=500", 'width="100%" ', 'frameborder="0" ', 'scrolling="no" ', 'allowfullscreen></iframe>', unsafe_allow_html=True)

def fetch_least_distance(lat,long):
    # Read the .xls file
    aed_locations = pd.read_excel('AED_locations_final.xlsx')
    aed_locations['distance_haversine'] =  aed_locations.apply(lambda x: haversine(float(lat),float(long),x.latitude,x.longitude), axis=1)
    index_min = aed_locations['distance_haversine'].idxmin()
    row_min = aed_locations.loc[index_min]
    return row_min

# """ 
# Formula of Haversine used here

# a = sin²(φB - φA/2) + cos φA * cos φB * sin²(λB - λA/2)
# c = 2 * atan2( √a, √(1−a) )
# d = R ⋅ c
# φ is latitude, λ is longitude, R is earth’s radius (mean radius = 6,371km)
# Coordinates in decimal degrees (e.g. 2.89078, 12.79797)
# """
def haversine(lat1, lon1, lat2, lon2):
    if (lat1 < -90 or lat1 > 90 or lat2 < -90 or lat2 > 90):
        raise ValueError("Latitude should be between -90 and 90")
    if(lon1 < -180 or lon1 > 180 or lon2 < -180 or lon2 > 180):
        raise ValueError("Longitude should be between -180 and 180")
    R = 6371000  # radius of Earth in meters
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)
    delta_phi = math.radians(abs(lat2 - lat1))
    delta_lambda = math.radians(abs(lon2 - lon1))
    a = math.sin(delta_phi / 2.0) * 2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2.0) * 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    meters = R * c  # output distance in meters
    km = meters / 1000.0  # output distance in kilometers
    return round(km, 3)




if __name__ == "__main__":
    main()
