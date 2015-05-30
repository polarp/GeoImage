import sys 
import json 
import requests
from os.path import isfile
from decimal import Decimal
from exifread import process_file

class ImageNotFound(Exception): pass
class CoordinatesNotFound(Exception): pass

class GeoImage(object):
    def __init__(self, path):
        self.image = Image(path)
        self.geocode = GeoCode()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            print exc_type, exc_value, traceback
        self.image.close()
        return self

    @property
    def address(self):
        return self.geocode.fetch_address(self.image.coordinates)

    @property
    def coordinates(self):
        return self.image.coordinates

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.image.file.name)

class GeoCode(object):
    def __init__(self, api_url=None, api_key=None):
        if api_url is None:
            self.api_url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng='
        self.api_key = api_key

    def fetch_address(self, coordinates):
        url = self.api_url + ','.join(coordinates)
        if self.api_key is not None:
            url = url + '&key=' + self.api_key

        request = requests.get(url)
        if request.status_code != requests.codes.ok:
            return None
        
        data = request.json()
        if len(data['results']) == len(list()):
            return None
        
        return data['results'][0]['formatted_address']

class Image(object):
    def __init__(self, path):
        if not isfile(path):
            raise ImageNotFound('Unable to open image!')
        self.file = open(path, 'rb')
        self.tags = process_file(self.file)

    @property
    def coordinates(self):
        tags = self.tags.copy()
        if tags.get('GPS GPSLatitude') is None:
            raise CoordinatesNotFound('Image does not contain coordinates metadata!')

        latitude = self._parse_coordinates(str(tags.get('GPS GPSLatitude')))    
        longitude = self._parse_coordinates(str(tags.get('GPS GPSLongitude')))
        return latitude, longitude

    def _parse_coordinates(self, coordinates):
        temp = coordinates[1:-1].replace(" ","").split(',')
        degrees = Decimal(temp[0])
        minutes = Decimal(temp[1])
        seconds = Decimal(temp[2].split('/')[0]) / Decimal(temp[2].split('/')[1])
        return str(degrees + minutes / 60 + seconds / 3600)

    def close(self):
        self.file.close()