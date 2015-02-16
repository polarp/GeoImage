import sys, exifread, json, requests, decimal

class GeoImage:
    def __init__(self, filename=None):
        if filename is None:
            print \
    """
    Initialized GeoImage without an actual image. 
    Use the get_info(filename = 'example.jpg') method to load image file. 
    """
        self.filename = filename
        self.errors = list()
        
    def get_info(self, filename=None):
        
        if self.filename is None and filename is None:
            raise ValueError, 'Image filename required in order to extract metadata'
        elif filename is not None:
            self.filename = filename
        self._process()
                
    def _parse_coordinates(self, coordinates):
        """ 
        Arguments: "coordinates" - represents the extracted coortinates string from the image meta data
           Return: string representation of the coordinates
        """ 
        temp = coordinates[1:-1].replace(" ","").split(',')
        degrees = decimal.Decimal(temp[0])
        minutes = decimal.Decimal(temp[1])
        seconds = decimal.Decimal(temp[2].split('/')[0]) / decimal.Decimal(temp[2].split('/')[1])
        return str( degrees + minutes / 60 + seconds / 3600 )

    def _get_coordinates(self, filedescriptor):
        """ 
        Arguments: "filedescriptor" - image file descriptor
           Return: tuple with the extracted coordinates(latitude, longitude)
        """    
        tags = exifread.process_file(filedescriptor) 
        if tags.get('GPS GPSLatitude') is None:
            self.errors.append("There isn't geo data located in the supplied image")
            return None
        latitude = self._parse_coordinates(str(tags.get('GPS GPSLatitude')))    
        longitude = self._parse_coordinates(str(tags.get('GPS GPSLongitude')))
        
        return latitude, longitude
    
    def _fetch_from_google(self, coordinates):
        """ 
        Arguments: "coordinates" - a tuple that contains longitude and latitude coordinates in string format
           Return: Places referring to the supplied coordinates from the google geolocation API
        """ 
        if coordinates is None:
            self.errors.append("Invalid coordinates")

        url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng='+','.join(coordinates)
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            data = r.json()
            if data['results'] == []:
                self.errors.append("No results found!")

            return self.filename + ' -> ' + data['results'][0]['formatted_address']    
    
    def _process(self):
        try:
            f = open(self.filename, 'rb')
            coordinates = self._get_coordinates(f)
            if coordinates != None:
                print self._fetch_from_google(coordinates)

        except IOError:
                self.errors.append("Unable to open image file!")
        finally:
            for error in self.errors:
                print error
            self.errors = list()