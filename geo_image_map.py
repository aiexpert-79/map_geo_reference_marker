import streamlit as st
import os
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import RendererAgg
from matplotlib.figure import Figure
from matplotlib.image import AxesImage
from ipyleaflet import Map, Marker, TileLayer, AwesomeIcon, SearchControl, FullScreenControl

class ImageClick:
    def __init__(self, image):
        # Initialize the ImageClick object with the provided image
        self.image = image
        self.click_count = 0
        self.coordinates = {}
        # Connect the click event to the __call__ method
        self.cid = image.figure.canvas.mpl_connect('button_press_event', self.handle_click)
        print("xxxxxxxxx", image, self.cid)
    
    def handle_click(self, event):
        # Handle the click event on the image
        print("===========")
        if event.inaxes != self.image.axes or self.click_count >= 3:
            return
        x = int(event.xdata)
        y = int(event.ydata)
        self.coordinates[f"{self.click_count + 1}"] = (x, y)
        self.click_count += 1
        print("==============", self.coordinates, self.click_count)

        if self.click_count == 3:
            st.write("Four clicks done!")
            # Disconnect the click event after three clicks
            self.image.figure.canvas.mpl_disconnect(self.cid)

def load_and_show_image(image_path):
    # Load and display the image, return the ImageClick instance for capturing clicks
    image = plt.imread(image_path)
    fig, ax = plt.subplots()
    ax.imshow(image)
    ax.set_title('Click on the image three times')
    click = ImageClick(ax.images[0])
    print(click.coordinates)
    ax.set_aspect('auto')
    plt.axis('off')
    plt.gca().set_aspect('auto')
    plt.gca().autoscale(enable=True)
    return fig, click

def create_map_with_markers():
    # Create a map instance with markers and controls
    pnoa_layer = TileLayer(url="https://tms-pnoa-ma.idee.es/1.0.0/pnoa-ma/{z}/{x}/{-y}.jpeg", name="PNOA")
    m = Map(center=(40, -4), zoom=6, layers=[pnoa_layer])
    m.add_control(FullScreenControl())
    marker_1 = Marker(location=[40, -4], draggable=True, icon=AwesomeIcon(name="map-marker", marker_color='darkblue', icon_color='white'))
    marker_2 = Marker(location=[40, -4.5], draggable=True, icon=AwesomeIcon(name="map-marker", marker_color='red', icon_color='white'))
    marker_3 = Marker(location=[40.5, -4], draggable=True, icon=AwesomeIcon(name="map-marker", marker_color='green', icon_color='white'))
    m.add_control(SearchControl(position="topleft", url='https://nominatim.openstreetmap.org/search?format=json&q={s}', zoom=14, marker=Marker(icon=AwesomeIcon(name="circle", marker_color='black', icon_color='white'), draggable=False)))
    m.add_layer(marker_1)
    m.add_layer(marker_2)
    m.add_layer(marker_3)
    return m, marker_1, marker_2, marker_3

def main():
    # Main function to coordinate image clicks and map interactions
    image_path = 'assets/boe_3_georeferenced.tif'
    fig, click = load_and_show_image(image_path)
    print(fig, click.coordinates)
    map_instance, marker_1, marker_2, marker_3 = create_map_with_markers()
    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    st.image(image, use_column_width=True)
    coordenadas_1 = marker_1.location
    coordenadas_2 = marker_2.location
    coordenadas_3 = marker_3.location
    print(coordenadas_1, coordenadas_2, coordenadas_3)
    st.write(coordenadas_1)
    st.write(coordenadas_2)
    st.write(coordenadas_3)
    if click.coordinates:
        pixel_x1, pixel_y1 = click.coordinates[1]
        map_y1, map_x1 = coordenadas_1
        pixel_x2, pixel_y2 = click.coordinates[2]
        map_y2, map_x2 = coordenadas_2
        pixel_x3, pixel_y3 = click.coordinates[3]
        map_y3, map_x3 = coordenadas_3
        # Perform georeferencing using gdal_translate and gdalwarp
        os.system(f"gdal_translate -of GTiff -a_srs EPSG:4326 -gcp {pixel_x1} {pixel_y1} {map_x1} {map_y1} -gcp {pixel_x2} {pixel_y2} {map_x2} {map_y2} -gcp {pixel_x3} {pixel_y3} {map_x3} {map_y3} imagen-sin-geo.tif output_georeferenced.tif")
        os.system("gdalwarp -of GTiff -t_srs EPSG:4326 output_georeferenced.tif georeferenced.tif")
        x, y = click.coordinates
        st.write(f"Clicked at ({x}, {y})")

if __name__ == "__main__":
    main()