from .utils import Image, GeoCode

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
    
    @property
    def latitude(self):
        return self.image.latitude

    @property
    def longitude(self):
        return self.image.longitude

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.image.file.name)


