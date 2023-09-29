import json
import requests

class WeatherData:
    def __init__(self, API_KEY, N_DAYS_FORECAST, location):
        self.API_KEY = API_KEY
        self.N_DAYS_FORECAST = N_DAYS_FORECAST
        self.location = location
        self.weather_data = None
        self.current_weather = None
        self.forecast_weather = []

    def fetch_data(self):
        """Fetch weather data from the API and store it."""
        try:
            url = f"http://api.weatherapi.com/v1/forecast.json?key={self.API_KEY}&q={self.location}&days={self.N_DAYS_FORECAST}&aqi=no&alerts=no"
            response = requests.get(url)
            if response.status_code == 200:
                self.weather_data = json.loads(response.content)
                self.current_weather = self.weather_data["current"]
                self.forecast_weather = self.weather_data["forecast"]["forecastday"]
            else:
                raise requests.RequestException(f"API request failed with status code: {response.status_code}")
        except Exception as e:
            raise Exception(f"Error fetching weather data: {e}")

    def get_current_weather(self):
        """
        Get the current weather data.

        Returns:
            dict: Current weather data.
        """
        return self.current_weather

    def get_forecast_weather(self, day):
        """
        Get the forecasted weather data for a particular day.

        Returns:
            dict: Forecasted weather data.
        """
        if 0 <= day < len(self.forecast_weather):
            return self.forecast_weather[day].get("day", {})
        return {}
        
