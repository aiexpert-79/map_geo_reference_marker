import streamlit as st
import os
import folium
from osgeo import gdal
from PIL import Image

def get_image_bounds(image_path):
    # Open the image using GDAL
    dataset = gdal.Open(image_path)
    if dataset is None:
        st.error("Could not open the image")
        return None
    # Extract geotransformation information to get image bounds
    geotransform = dataset.GetGeoTransform()
    min_x = geotransform[0]
    max_x = min_x + geotransform[1] * dataset.RasterXSize
    max_y = geotransform[3]
    min_y = max_y + geotransform[5] * dataset.RasterYSize
    # Define bounds dictionary
    bounds = {
        "min_x": min_x,
        "max_x": max_x,
        "min_y": min_y,
        "max_y": max_y
    }
    # Convert bounds to corner coordinates
    esquina_inf_izq = (bounds['min_y'], bounds['min_x'])
    esquina_sup_der = (bounds['max_y'], bounds['max_x'])
    return [esquina_inf_izq, esquina_sup_der]

def tif_to_png(input_path, output_path):
    # Convert TIF image to PNG format using PIL
    image_tif = Image.open(input_path)
    image_tif.save(output_path)
    return output_path

def create_folium_map(image_tif):
    # Create a folium map with a raster layer overlay
    m = folium.Map(location=[40, -4], zoom_start=8,
                   tiles="https://tms-pnoa-ma.idee.es/1.0.0/pnoa-ma/{z}/{x}/{-y}.jpeg",
                   attr="PNOA",)

    # Convert TIF to PNG and get image bounds
    image_png = tif_to_png(image_tif, 'imagen.png')
    bounds = get_image_bounds(image_tif)

    # Check if PNG file exists and add it to the folium map
    if not os.path.isfile(image_png):
        st.error(f"Could not find {image_png}")
    else:
        img = folium.raster_layers.ImageOverlay(
            name=image_png,
            image=image_png,
            bounds=bounds,
            opacity=0.6,
            interactive=True,
            cross_origin=False,
            zindex=1,
        )
        img.add_to(m)

        # Add 3 markers to the map
        marker_locations = [[40.1, -4.2], [40.2, -4.3], [40.3, -4.4]]
        marker_list = []
        for marker_location in marker_locations:
            marker = folium.Marker(location=marker_location, popup=folium.Popup(str(marker_location)))
            marker.add_to(m)
            marker_list.append(marker)
        
        folium.LayerControl().add_to(m)

    return m

def main():
    # Main function to create folium map from a TIF image
    image_tif = "assets/boe_3_georeferenced.tif"
    folium_map = create_folium_map(image_tif)
    folium_map.save('map.html')

    # Display the map using Streamlit
    map_html = open('map.html', 'r').read()
    st.components.v1.html(map_html, width=800, height=600)

if __name__ == "__main__":
    main()