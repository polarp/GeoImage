from geoimage import GeoImage
import os

# Create image path
image_1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sigur_ros.jpg')
# Init GeoImage instance
locator = GeoImage(filename=image_1)
# Print metadata
locator.get_info()

image_2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'thievery_corporation.jpg')
locator.get_info(filename=image_2)