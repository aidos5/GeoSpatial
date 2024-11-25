from geopy.geocoders import Nominatim

# Initialize geolocator
geolocator = Nominatim(user_agent="geoapi")

# List of place names

def get_coordinates(place_names):
    coordinates = {}
    for place in place_names:
        location = geolocator.geocode(place)
        if location:
            coordinates[place] = (location.latitude, location.longitude)

    return coordinates
