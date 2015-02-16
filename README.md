GeoImage
========

GeoImage is a simple tool that reads metadata from an image and prints the address using google's reverse geocoding api

## Requirements

To install the nececary requirements in order to use GeoImage type:
```bash
# pip install -r requirements.txt
```

## Usage

To create a bloom filter, choose an approximate capacity and an acceptable error rate.

```python
>>> from geoimage import GeoImage
>>> locator = GeoImage(filename="image_filename")
>>> locator.get_info()
```

Additionaly you can pass image filename to the get_info method if you want to extract data from different image


