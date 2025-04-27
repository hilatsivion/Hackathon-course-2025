from geopy.geocoders import Nominatim

# Initialize geocoder
geolocator = Nominatim(user_agent="app.py")

def get_lat_lon(settlement_name):
    try:
        location = geolocator.geocode(f"{settlement_name}, Israel")
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        print(f"Error during geocoding: {e}")
        return None, None

# Example usage
# latitude, longitude = get_lat_lon("חבצלת השרון")
# print(latitude, longitude)

