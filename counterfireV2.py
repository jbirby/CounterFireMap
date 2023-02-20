import folium
import pandas as pd
import mgrs
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
import os
import math

# Define the date and time for the output file name
now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Create a GUI file dialog to select the input file
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(filetypes=[('CSV files', '*.csv')])

# Read in the CSV file
df = pd.read_csv(file_path)

# Create a new map centered on the first POO point
poo_mgrs = df['POO'].iloc[0]
poo_lat, poo_lon = mgrs.MGRS().toLatLon(poo_mgrs)
m = folium.Map(location=[poo_lat, poo_lon], zoom_start=10, control_scale=True)

# Define a function to calculate the distance between two (lat, lon) pairs using the Haversine formula
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0088  # Earth's radius in km
    phi1, phi2 = lat1 * math.pi/180, lat2 * math.pi/180
    dphi = (lat2 - lat1) * math.pi/180
    dlambda = (lon2 - lon1) * math.pi/180
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R*c
    return d

# Create a dictionary to store feature groups for each type
type_groups = {}

# Create a dictionary to store lines for each POO type
line_groups = {}

# Loop through the rows and plot each point on the map
for index, row in df.iterrows():
    poo_mgrs = row['POO']
    poi_mgrs = row['POI']
    dtg = row['DTG']
    poo_type = row['TYPE']
    system = row['SYSTEM']
    
    # Convert MGRS coordinates to (lat, lon) pairs
    poo_lat, poo_lon = mgrs.MGRS().toLatLon(poo_mgrs)
    poi_lat, poi_lon = mgrs.MGRS().toLatLon(poi_mgrs)
    
    # Determine the POO marker icon based on the type
    if poo_type == 'ROCKET':
        poo_icon = folium.Icon(color='red', icon='fa-solid fa-r', prefix='fa')
    elif poo_type == 'MORTAR':
        poo_icon = folium.Icon(color='red', icon='fa-solid fa-m', prefix='fa')
    elif poo_type == 'ARTY':
        poo_icon = folium.Icon(color='red', icon='fa-solid fa-a', prefix='fa')
    else:
        poo_icon = folium.Icon(color='red')
    
    # Create a new feature group for the POO type if it doesn't exist yet
    if poo_type not in type_groups:
        type_groups[poo_type] = folium.FeatureGroup(name=poo_type)
        line_groups[poo_type] = folium.FeatureGroup(name=f"{poo_type} lines")
    
    # Add POI and POO markers to the appropriate feature group
    poo_popup_text = f"MGRS: {poo_mgrs}, DTG: {dtg}, SYSTEM: {system}"
    poi_popup_text = f"MGRS: {poi_mgrs}, DTG: {dtg}, SYSTEM: {system}"
    poo_popup = folium.Popup(poo_popup_text, parse_html=True)
    poi_popup = folium.Popup(poi_popup_text, parse_html=True)
    poo_marker = folium.Marker(location=[poo_lat, poo_lon], popup=poo_popup, tooltip='POO', icon=poo_icon)
    poi_marker = folium.Marker(location=[poi_lat, poi_lon], popup=poi_popup, tooltip='POI', icon=folium.Icon(color='green', icon='fa-sharp fa-solid fa-explosion', prefix='fa'))
    poo_marker.add_to(type_groups[poo_type])
    poi_marker.add_to(type_groups[poo_type])
    
    # Calculate the distance between the POO and POI and add it to the popup
    distance = haversine(poo_lat, poo_lon, poi_lat, poi_lon)
    distance_text = f"Distance: {distance:.2f} km"
    distance_html = folium.Html(f"{distance_text}")
    distance_popup = folium.Popup(distance_html, parse_html=True)
    distance_marker = folium.Marker(location=[(poo_lat + poi_lat)/2, (poo_lon + poi_lon)/2], popup=distance_popup, tooltip='Distance', icon=folium.Icon(color='purple', icon='fa', prefix='fa', icon_size=(15, 15)), show=False)
    distance_marker.add_to(type_groups[poo_type])
    
    # Add a line between the POO and POI to the appropriate line group
    line = folium.PolyLine(locations=[[poo_lat, poo_lon], [poi_lat, poi_lon]], color='blue', weight=2)
    if poo_type not in line_groups:
        line_groups[poo_type] = folium.FeatureGroup(name=f"{poo_type} lines")
    line.add_to(line_groups[poo_type])

# Add the type feature groups and line groups to the map and the layer control
for group in type_groups.values():
    m.add_child(group)
for group in line_groups.values():
    m.add_child(group)

# Add a layer control to toggle POO types and lines
folium.LayerControl(collapsed=True).add_to(m)

# Save the map as an HTML file on the desktop
output_file = os.path.expanduser(f"~/Desktop/CounterFire_{now}.html")
m.save(output_file)

# Display the map
m


