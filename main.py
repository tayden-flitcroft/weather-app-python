import geocoder
import os
from weather import Weather
from location import Location, Coordinates

def __main__():
    # determine location selection based on ip
    g = geocoder.ip('me')
    ip_city = g.city
    ip_state = g.state
    ip_coordinates = g.latlng

    location_confirmation = input(f'Check the weather for your current location ({g.city}, {g.state}): (y/n) ')

    # anything other than 'n' or 'no' will proceed with ip location data
    if location_confirmation.lower() == 'n' or location_confirmation.lower() == 'no':
        # Collect City and State from user via input
        city_name = input('Enter the City: ')
        state_name = input('Enter the State: ')
        location = Location(city_name, state_name)
    else:
        city_name = ip_city
        state_name = ip_state
        location = Location(city_name, state_name, Coordinates(ip_coordinates[0], ip_coordinates[1]))

    # initialize Weather with location data
    weather = Weather(location)
    # fetch forecast data from weather class
    forecast = weather.get_weather_data_forecast()

    # initiailize headers for returned text
    current_weather_header = f"Weather Information for {location}"
    forecast_header = f"{weather.forecast_days}-Day Forecast"

    # clear console to clean up terminal ui
    os.system('cls' if os.name=='nt' else 'clear')

    # build current weather data text template
    weather_text = f'''
    {"-"*len(current_weather_header)}
    {current_weather_header}
    {"-"*len(current_weather_header)}

    Temperature: {weather.data.temperature}
    Feels Like: {weather.data.feels_like_temp}

    Conditions:
        Precipitation: {weather.data.precipitation}
        Rain: {weather.data.rain}
        Snow: {weather.data.snow}

        Wind Speed: {weather.data.wind_speed}
        Wind Direction: {weather.data.wind_direction}
    '''

    # initialize forecast text template with header
    forecast_data_text = f'''
    {"-"*len(forecast_header)}
    {forecast_header}
    {"-"*len(forecast_header)}
    '''

    # iterate over each days data and append forecast_data_text with daily data
    for forecast_data in forecast:
        forecast_data_text += f'''
    {forecast_data.date}:
        Highest Temperature: {forecast_data.temp_max},
        Lowest Temperature: {forecast_data.temp_min},
        Precipitation: {forecast_data.total_precipitation},
        Sunrise: {forecast_data.sunrise},
        Sunset: {forecast_data.sunset}            
        '''
        
    # output completed text template
    print(weather_text + forecast_data_text)

if __name__ == "__main__":
    __main__()