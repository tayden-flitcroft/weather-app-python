import requests
from datetime import datetime

class Sanitize_Weather_Data:
    def __init__(self, raw_value, unit):
        self.raw_value = raw_value
        self.unit = unit
    
    def __str__(self):
        return f"{self.raw_value} {self.unit}"
    
class Weather_Data_Forecast:
    def __init__(self, api_data, idx):
        self.date = datetime.strptime(api_data['daily']['time'][idx], "%Y-%m-%d").strftime("%B %d")
        self.temp_max = f"{api_data['daily']['temperature_2m_max'][idx]}{api_data['daily_units']['temperature_2m_max']}"
        self.temp_min = f"{api_data['daily']['temperature_2m_min'][idx]}{api_data['daily_units']['temperature_2m_min']}"
        self.total_precipitation = f"{api_data['daily']['precipitation_sum'][idx]} {api_data['daily_units']['precipitation_sum']}"
        self.sunrise = f'{datetime.strptime(api_data["daily"]["sunrise"][idx], "%Y-%m-%dT%H:%M").strftime("%I:%M %p")} {api_data["timezone_abbreviation"]}'
        self.sunset = f'{datetime.strptime(api_data["daily"]["sunset"][idx], "%Y-%m-%dT%H:%M").strftime("%I:%M %p")} {api_data["timezone_abbreviation"]}'

class Weather_Data:
    def __init__(self, api_data):
        self.data = api_data
        self.feels_like_temp = self.sanitize_weather_data('apparent_temperature')
        self.rain = self.sanitize_weather_data('rain')
        self.precipitation = self.sanitize_weather_data('precipitation')
        self.snow = self.sanitize_weather_data('snowfall')
        self.temperature = self.sanitize_weather_data('temperature_2m')
        self.wind_direction = self.sanitize_weather_data('wind_direction_10m')
        self.wind_speed = self.sanitize_weather_data('wind_speed_10m')

    # this will clean up the data to provide a more human accessible key as well as package both the raw data as object keys and a pre formatted string that can be used that includes the value and the metric
    def sanitize_weather_data(self, key):
        return Sanitize_Weather_Data(self.data['current'][key], self.data['current_units'][key])

class Weather:
    def __init__(self, location, forecast_days = 7):
        self.latitude = location.coordinates.latitude
        self.longitude = location.coordinates.longitude
        self.data = self.get_weather_data_current()
        self.forecast_days = forecast_days
    
    def get_weather_data_current(self):
        # make API request to get current weather data
        response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={self.latitude}&longitude={self.longitude}&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,rain,showers,snowfall,wind_speed_10m,wind_direction_10m&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch")

        # validate successful response code
        if response.status_code == 200:
            json = response.json()

            # map over API response and change object keys to match my schema and provide a preformatted string that includes the raw value and unit
            return Weather_Data(json)
        else:
            # handle error when fetching current weather data fails
            print(f"ERROR: ERROR GETTING WEATHER DATA response_code:{response.status_code}")
            exit()
    
    def get_weather_data_forecast(self):
        # make API request to fetch forecast weather data
        response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={self.latitude}&longitude={self.longitude}&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_sum,rain_sum,showers_sum,snowfall_sum,precipitation_probability_max&timezone=auto&forecast_days={self.forecast_days}&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch")

        # validate successful response code
        if response.status_code == 200:
            json = response.json()

            # initialize loop index & data array
            idx = 0
            data = []

            # iterate over each item in response body as each returned item will have a length == forecast_days
            while idx < self.forecast_days:
                # append Weather_Data_Forecast object to data array and increment idx until loop condition fails
                data.append(Weather_Data_Forecast(json, idx))
                idx += 1

            return data
        else:
            # handle error when fetching forecast data
            print(f"ERROR: THERE WAS A PROBLEM GETTING THE FORECAST DATA response_code:{response.status_code}")
            exit()