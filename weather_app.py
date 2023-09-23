import json
import requests
from datetime import datetime
from tkinter import *
from PIL import Image, ImageTk

API_KEY = "04cefdc70dc64f37bf001213232309"
N_DAYS_FORECAST = 2

class WeatherApp(Tk):
    def __init__(self):
        super().__init__()
        self.title("Weather App")
        self.geometry("640x480")
        self.create_widgets()

    def create_widgets(self):
        Label(self, text="Enter City, State or Country: ").grid(row = 0, column = 0, sticky="nsew")
        self.location_entry = Entry(self, width = 20)
        self.location_entry.grid(row = 0, column = 1, sticky="nsew")
        Button(self, text="Get Weather", command=self.get_weather).grid(row = 0, column = 2, sticky="nsew")

        Label(self, text= "").grid(row = 1, column = 0, columnspan=3, sticky="nsew")

        self.today_label = Label(self, text = "")
        self.today_label.grid(row = 2, column = 0, columnspan=3, sticky="nsew")

        self.weather_icon = Label(self)
        self.weather_icon.grid(row = 3, column = 0, columnspan=3, sticky="nsew")

        self.condition_label = Label(self, text = "")
        self.condition_label.grid(row = 4, column = 0, columnspan=3, sticky="nsew")

        self.temperature_label = Label(self, text = "")
        self.temperature_label.grid(row = 5, column = 0, columnspan=3, sticky="nsew")

        self.wind_label = Label(self, text = "")
        self.wind_label.grid(row = 6, column = 0, columnspan=3, sticky="nsew")

        self.humidity_label = Label(self, text = "")
        self.humidity_label.grid(row = 7, column = 0, columnspan=3, sticky="nsew")

        Label(self, text=" ").grid(row = 8, column = 0, columnspan=3, sticky="nsew")

        self.forecast_icon = Label(self)
        self.forecast_icon.grid(row = 9, column = 0, columnspan=3, sticky="nsew")

        self.forecast_condition_label = Label(self, text = "")
        self.forecast_condition_label.grid(row = 10, column = 0, columnspan=3, sticky="nsew")

        self.max_temperature_label = Label(self, text = "")
        self.max_temperature_label.grid(row = 11, column = 0, columnspan=3, sticky="nsew")

        self.min_temperature_label = Label(self, text = "")
        self.min_temperature_label.grid(row = 12, column = 0, columnspan=3, sticky="nsew")

        self.forecast_wind_label = Label(self, text = "")
        self.forecast_wind_label.grid(row = 13, column = 0, columnspan=3, sticky="nsew")

        self.avg_humidity_label = Label(self, text="")
        self.avg_humidity_label.grid(row=14, column=0, columnspan=3, sticky="nsew")

        self.chance_rain_label = Label(self, text = "")
        self.chance_rain_label.grid(row = 15, column = 0, columnspan=3, sticky="nsew")

        self.error_label = Label(self, text = "")
        self.error_label.grid(row = 16, column = 0, columnspan=3, sticky="nsew")

    def retrieve_weather_data(self, location):
        try:
            if not location:
                raise ValueError("Location cannot be empty!")

            url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={location}&days={N_DAYS_FORECAST}&aqi=no&alerts=no"
            response = requests.get(url)
            if response.status_code == 200:
                return json.loads(response.content)
            else:
                raise ValueError(f"API request failed with status code {response.status_code}")
        except ValueError as e:
            raise e
        except Exception as e:
            raise e

    def download_icon(self, url, filename):
        try:
            response = requests.get(url, stream = True)
            if response.status_code == 200:
                with open(filename, "wb") as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
        except Exception as e:
            self.error_label.config(f"Error ocurred downloading icon: {e}")

    def get_weather(self):
        try:
            self.error_label.config(text = "")

            location = self.location_entry.get()
            weather = self.retrieve_weather_data(location)

            if weather:
                current_weather = weather["current"]

                self.today_label.config(text = "Today's Weather")
                self.condition_label.config(text = f"Current Condition: {current_weather['condition']['text']}")
                self.temperature_label.config(text = f"Current Temperature: {current_weather['temp_f']}°F | {current_weather['temp_c']}°C")
                
                self.wind_label.config(text = f"Current Wind: {current_weather['wind_mph']}mph | {current_weather['wind_kph']}kph {current_weather['wind_dir']}")
                self.humidity_label.config(text = f"Current Humidity: {current_weather['humidity']}%")

                self.download_icon(f"http:{current_weather['condition']['icon']}", "current_icon.png")
                current_icon = ImageTk.PhotoImage(file = "current_icon.png")
                self.weather_icon.config(image = current_icon)
                self.weather_icon.image = current_icon

                forecast_weather = weather["forecast"]["forecastday"][1]["day"]

                self.forecast_condition_label.config(text = f"Forecast Condition: {forecast_weather['condition']['text']}")
                self.max_temperature_label.config(text = f"Max Temperature: {forecast_weather['maxtemp_f']}°F | {forecast_weather['maxtemp_c']}°C")
                self.min_temperature_label.config(text = f"Min Temperature: {forecast_weather['mintemp_f']}°F| {forecast_weather['maxtemp_c']}°C")
                self.forecast_wind_label.config(text = f"Max Wind: {forecast_weather['maxwind_mph']}mph | {forecast_weather['maxwind_kph']}kph")
                self.avg_humidity_label.config(text = f"Average Humidity: {forecast_weather['avghumidity']}%")
                self.chance_rain_label.config(text = f"Chance of Rain: {forecast_weather['daily_chance_of_rain']}%")

                self.download_icon(f"http:{forecast_weather['condition']['icon']}", "forecast_icon.png")
                forecase_icon = ImageTk.PhotoImage(file = "forecast_icon.png")
                self.forecast_icon.config(image = forecase_icon)
                self.forecast_icon.image = forecase_icon
        except Exception as e:
            self.error_label.config(text=f"Unable to retrieve weather data. {e}")

if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()
