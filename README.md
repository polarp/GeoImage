GeoImage
========

GeoImage is a simple library that reads image metadata and extracts the address and the coordinates using google's reverse geocoding api

## Requirements

To install the necessary requirements in order to use GeoImage type:
```bash
# pip install -r requirements.txt
```

## Usage

```python
>>> from geoimage import GeoImage
>>> with GeoImage('sigur_ros.jpg') as gi:
...     print gi.address
...     print gi.coordinates
... 
Trg Leona Štuklja 5, 2000 Maribor, Slovenia
('46.55915277777777777777777778', '15.64904083333333333333333333')
>>> gi = GeoImage('sigur_ros.jpg')
>>> print gi.address
Trg Leona Štuklja 5, 2000 Maribor, Slovenia
>>> 
```



