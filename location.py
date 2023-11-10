import requests

class Coordinates:
    def __init__(self, latitude, longitude):
        self.longitude = longitude
        self.latitude = latitude

    def __str__(self):
        return f"latitude: {self.latitude}, longitude: {self.longitude}"

class Location:
    def __init__(self, city, state, coordinates = None):
        self.city = city
        self.state = state
        self.coordinates = coordinates or self.get_coordinates()

    def get_coordinates(self):
        # Make API call to collect longitude/latitude coordinates
        response = requests.get(f'https://geocoding-api.open-meteo.com/v1/search?name={self.city}')

        # Validate successful response
        if response.status_code == 200:

            # Convert response to JSON
            json = response.json()

            # validate successful response contains results
            if 'results' in json:
                if [result for result in json['results'] if result['admin1'].lower() == self.state.lower()]:
                    # Destructure city_data by filtering the response to locate the object that matches the state name just in case there are mulitple of the same city across the country
                    city_data = [result for result in json['results'] if result['admin1'].lower() == self.state.lower()][0]

                    # Redefine variables to syncronize with API values
                    self.state = city_data['admin1']
                    self.city = city_data['name']

                    # assign coordinates to object
                    return Coordinates(city_data['latitude'], city_data['longitude'])
                else:
                    # Successful call to geocoding API with a list of results, but no city/state combo matching what the use provided was found
                    print(f'ERROR: CITY: {self.city.title()} WAS FOUND, BUT WAS NOT FOUND IN YOUR CHOSEN STATE: {self.state.capitalize()}. PLEASE VALIDATE YOUR ENTRY AND TRY AGAIN.')
                    exit()
            else:
                # Successful call to geocoding API but no value was returned
                print(f'ERROR: CITY: {self.city.title()} WAS NOT FOUND. PLEASE TRY AGAIN.')
                exit()
        else:
            # Failed network call to geocoding API
            print(f"ERROR: ERROR GETTING COORDINATES response_code:{response.status_code}")
            exit()

    def __str__(self):
        return f"{self.city.title()}, {self.state.capitalize()}"