import streamlit as st
import streamlit.components.v1 as components

# Setup markers.
locations = [[40, -4], [40, -4.5], [40.5, -4], [40.5, -4.5]]
markers = [f"marker{i}" for i in range(len(locations))]

# Create Streamlit app.
st.set_page_config(layout="wide")

# Define the HTML template for the map.
map_html = f"""
    <div id="map" style="width: 1000px; height: 500px;"></div>
    <script>
        function updateMap() {{
            var markers = {markers};
            var locations = {locations};
            var map = L.map('map').setView([40.25, -4.25], 14);
            L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/{{z}}/{{x}}/{{y}}?access_token=YOUR_MAPBOX_ACCESS_TOKEN', {{
                tileSize: 512,
                zoomOffset: -1,
                accessToken: 'YOUR_MAPBOX_ACCESS_TOKEN'
            }}).addTo(map);
            for (var i = 0; i < markers.length; i++) {{
                var marker = markers[i];
                var location = locations[i];
                L.marker(location).addTo(map).on('click', function() {{
                    Streamlit.setComponentValue(marker);
                }});
            }}
        }}
        updateMap();
    </script>
"""

# Display the map and the log.
components.html(map_html)
log = st.empty()

# Check for marker clicks.
marker_value = st.session_state.get("marker_value", None)
if marker_value is not None:
    location = locations[int(marker_value[6:])]
    log.write(location)  # Print location to the Streamlit app