import streamlit as st
from streamlit_folium import folium_static
import folium
import pandas as pd


# if "radius" not in st.session_state:
#     st.session_state.radius = "0.5"

# st.set_page_config(layout = 'wide')
if "radius" not in st.session_state:
    st.session_state.radius = "100 meters"

def miles_to_meters(miles):
    return miles*1

iconLadbrokes = folium.features.CustomIcon('Ladbrokes_logo.png', icon_size=(100,100))

df_500_gc= pd.read_csv('distances_500_gc5.csv')

print(df_500_gc)

m =folium.Map(location=[55.8642, -4.2518],zoom_start=12)

data = {
    "No radius": 0,
    "100 meters": 100,
    "200 meters": 200,
    "300 meters": 300,
    "500 meters": 500
}

radius = miles_to_meters(data[st.session_state.radius])


for k, el in enumerate(df_500_gc['Lb_name']):
    # Determine the type of shop based on the name column
    if df_500_gc['Lb_name'].iloc[k] != '':
        lb_lat = df_500_gc['Lb_latitude'].iloc[k]
        lb_lon = df_500_gc['Lb_longitude'].iloc[k]
    else:
        continue
    iconLadbrokes = folium.features.CustomIcon('Ladbrokes_logo.png', icon_size=(20,20))
    popupLadbrokes= f"<br>Shop: {df_500_gc['Lb_name'].iloc[k]}<br><br>One Coral shop within 500m: {df_500_gc['Cr_name'].iloc[k]}<br><br>Straight Distance (m): {df_500_gc['great-circle distance'].iloc[k]}<br><br>Walking Distance: {df_500_gc['walking_distance_in_km'].iloc[k]}, Estimated time: {df_500_gc['walking_time_in_min'].iloc[k]}<br><br>Car Distance: {df_500_gc['car_distance_in_km'].iloc[k]}, Estimated time: {df_500_gc['car_time_in_min'].iloc[k]}<br>"
    folium.Marker(location=[lb_lat, lb_lon], popup=popupLadbrokes, tooltip='click for more information',
                  icon=iconLadbrokes).add_to(m)
    folium.Circle([lb_lat, lb_lon],
                radius=radius,
                popup=f'{radius}m',
                clor='red',
                fill=True,
                opacity=0.025,
                ).add_to(m)

for k, el in enumerate(df_500_gc['Cr_name']):
    # Determine the type of shop based on the name column
    if df_500_gc['Cr_name'].iloc[k] != '':
        cr_lat = df_500_gc['Cr_latitude'].iloc[k]
        cr_lon = df_500_gc['Cr_longitude'].iloc[k]
    else:
        continue
    iconLadbrokes = folium.features.CustomIcon('coral_logo.jpg', icon_size=(20,20))
    popupLadbrokes= f"<strong> Coral shop name:  {df_500_gc['Cr_name'].iloc[k]}</strong><br>{df_500_gc['Cr_name'].iloc[k]}<br>"
    folium.Marker(location=[cr_lat, cr_lon], popup=popupLadbrokes, tooltip='click for more information',
                  icon=iconLadbrokes).add_to(m)

st.title('Frontier economics task for Data Science Job')
st.sidebar.selectbox(
    label="What radius do you want to assign?",
    options=("100 meters", "200 meters", "300 meters", "500 meters"),
    key="radius"
)

radius = miles_to_meters(data[st.session_state.radius])


# folium.Marker([lat, lon]).add_to(m)
# folium.Circle([lat, lon], radius=radius).add_to(m)  # radius is in meters

folium_static(m)
