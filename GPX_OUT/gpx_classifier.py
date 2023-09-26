import gpxpy
import pandas as pd
from geopy.geocoders import Nominatim
import folium

# Initialize a geocoder
geolocator = Nominatim(user_agent="my_application")

# Loop over all GPX files
for file_name in gpx_file_names:
    # Parse the GPX file
    with open(file_name, "r") as f:
        gpx = gpxpy.parse(f)

    # Extract the location information from the GPX file
    latitudes = []
    longitudes = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                latitudes.append(point.latitude)
                longitudes.append(point.longitude)

    # Convert the location information into human-readable addresses
    addresses = []
    for latitude, longitude in zip(latitudes, longitudes):
        location = geolocator.reverse(f"{latitude}, {longitude}")
        addresses.append(location.address)

    # Store the data in a Pandas DataFrame
    data = pd.DataFrame({"latitude": latitudes, "longitude": longitudes, "address": addresses})

    # Create a map with Folium
    map_center = [latitudes[0], longitudes[0]]
    m = folium.Map(location=map_center, zoom_start=12)
    for i, row in data.iterrows():
        folium.Marker(location=[row["latitude"], row["longitude"]], popup=row["address"]).add_to(m)

    # Save the map as an HTML file
    m.save(f"{file_name}.html")
