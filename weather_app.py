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

        self.weather_labels = []
        self.create_weather_labels(row_start = 2, column_start = 0, columnspan = 3)

    def create_weather_labels(self, row_start, column_start, columnspan):
        labels = [
            ("", row_start), # Today's label 
            (self.weather_icon, row_start + 1), # Today's weather icon
            ("", row_start + 2), # Today's condition
            ("", row_start + 3), # Today's temperature
            ("", row_start + 4), # Today's wind speed
            ("", row_start + 5), # Today's humidity
            ("", row_start + 6), # Spacer label to create a gap between today's cast and forecast
            (self.forecast_icon, row_start + 7),  # Forecast icon
            ("", row_start + 8), # Forecast condition
            ("", row_start + 9), # Forecast max temperature
            ("", row_start + 10), # Forecast min temperature
            ("", row_start + 11), # Forecast wind speed
            ("", row_start + 12), # Forecast humidity
            ("", row_start + 13), # Forecast rain chance
            ("", row_start + 14), # Spacer label to create a gap between forecast and error label
            (self.error_label, row_start + 15), # Forecast error lable
        ]

        for text, row in labels:
            label = Label(self, text = text)
            label.grid(row = row, column = column_start, columnspan = columnspan, sticky="nsew")
            self.weather_labels.append(label)

        # self.today_label = Label(self, text = "")
        # self.today_label.grid(row = 2, column = 0, columnspan=3, sticky="nsew")

        # self.weather_icon = Label(self)
        # self.weather_icon.grid(row = 3, column = 0, columnspan=3, sticky="nsew")

        # self.condition_label = Label(self, text = "")
        # self.condition_label.grid(row = 4, column = 0, columnspan=3, sticky="nsew")

        # self.temperature_label = Label(self, text = "")
        # self.temperature_label.grid(row = 5, column = 0, columnspan=3, sticky="nsew")

        # self.wind_label = Label(self, text = "")
        # self.wind_label.grid(row = 6, column = 0, columnspan=3, sticky="nsew")

        # self.humidity_label = Label(self, text = "")
        # self.humidity_label.grid(row = 7, column = 0, columnspan=3, sticky="nsew")

        # Label(self, text=" ").grid(row = 8, column = 0, columnspan=3, sticky="nsew")

        # self.forecast_icon = Label(self)
        # self.forecast_icon.grid(row = 9, column = 0, columnspan=3, sticky="nsew")

        # self.forecast_condition_label = Label(self, text = "")
        # self.forecast_condition_label.grid(row = 10, column = 0, columnspan=3, sticky="nsew")

        # self.max_temperature_label = Label(self, text = "")
        # self.max_temperature_label.grid(row = 11, column = 0, columnspan=3, sticky="nsew")

        # self.min_temperature_label = Label(self, text = "")
        # self.min_temperature_label.grid(row = 12, column = 0, columnspan=3, sticky="nsew")

        # self.forecast_wind_label = Label(self, text = "")
        # self.forecast_wind_label.grid(row = 13, column = 0, columnspan=3, sticky="nsew")

        # self.avg_humidity_label = Label(self, text="")
        # self.avg_humidity_label.grid(row=14, column=0, columnspan=3, sticky="nsew")

        # self.chance_rain_label = Label(self, text = "")
        # self.chance_rain_label.grid(row = 15, column = 0, columnspan=3, sticky="nsew")

        # self.error_label = Label(self, text = "")
        # self.error_label.grid(row = 16, column = 0, columnspan=3, sticky="nsew")

    def get_weather(self):
        try:
            self.error_label.config(text = "")

            location = self.location_entry.get()
            weather_data = WeatherData(API_KEY, location)
            weather_data.fetch_data()

            current_weather = weather_data.get_current_weather()
            forecast_weather = weather_data.get_forecast_weather()

            self.update_labels(current_weather, forecast_weather)
        except Exception as e:
            self.error_label.config(text = f"Unable to retrieve weather data.\n Error {e}.")

        #     if weather:
        #         current_weather = weather["current"]

        #         self.today_label.config(text = "Today's Weather")
        #         self.condition_label.config(text = f"Current Condition: {current_weather['condition']['text']}")
        #         self.temperature_label.config(text = f"Current Temperature: {current_weather['temp_f']}°F | {current_weather['temp_c']}°C")
                
        #         self.wind_label.config(text = f"Current Wind: {current_weather['wind_mph']}mph | {current_weather['wind_kph']}kph {current_weather['wind_dir']}")
        #         self.humidity_label.config(text = f"Current Humidity: {current_weather['humidity']}%")

        #         self.download_icon(f"http:{current_weather['condition']['icon']}", "current_icon.png")
        #         current_icon = ImageTk.PhotoImage(file = "current_icon.png")
        #         self.weather_icon.config(image = current_icon)
        #         self.weather_icon.image = current_icon

        #         forecast_weather = weather["forecast"]["forecastday"][1]["day"]

        #         self.forecast_condition_label.config(text = f"Forecast Condition: {forecast_weather['condition']['text']}")
        #         self.max_temperature_label.config(text = f"Max Temperature: {forecast_weather['maxtemp_f']}°F | {forecast_weather['maxtemp_c']}°C")
        #         self.min_temperature_label.config(text = f"Min Temperature: {forecast_weather['mintemp_f']}°F| {forecast_weather['maxtemp_c']}°C")
        #         self.forecast_wind_label.config(text = f"Max Wind: {forecast_weather['maxwind_mph']}mph | {forecast_weather['maxwind_kph']}kph")
        #         self.avg_humidity_label.config(text = f"Average Humidity: {forecast_weather['avghumidity']}%")
        #         self.chance_rain_label.config(text = f"Chance of Rain: {forecast_weather['daily_chance_of_rain']}%")

        #         self.download_icon(f"http:{forecast_weather['condition']['icon']}", "forecast_icon.png")
        #         forecase_icon = ImageTk.PhotoImage(file = "forecast_icon.png")
        #         self.forecast_icon.config(image = forecase_icon)
        #         self.forecast_icon.image = forecase_icon
        # except Exception as e:
        #     self.error_label.config(text=f"Unable to retrieve weather data. {e}")

    def update_labels(self, current_weather, forecast_weather):
        label_text = [
            "Today's Weather",
            f"http:{current_weather['condition']['icon']}",
            f"Current Temperature: {current_weather['temp_f']}°F | {current_weather['temp_c']}°C",
            f"Current Wind: {current_weather['wind_mph']}mph | {current_weather['wind_kph']}kph {current_weather['wind_dir']}",
            f"Current Humidity: {current_weather['humidity']}%",
            "",
            f"http:{forecast_weather['condition']['icon']}",
            f"Forecast Condition: {forecast_weather['condition']['text']}",
            f"Max Temperature: {forecast_weather['maxtemp_f']}°F | {forecast_weather['maxtemp_c']}°C",
            f"Min Temperature: {forecast_weather['mintemp_f']}°F| {forecast_weather['maxtemp_c']}°C",
            f"Max Wind: {forecast_weather['maxwind_mph']}mph | {forecast_weather['maxwind_kph']}kph",
            f"Average Humidity: {forecast_weather['avghumidity']}%",
            f"Chance of Rain: {forecast_weather['daily_chance_of_rain']}%",
            ""
        ]

        for i in range(len(self.weather_labels)):
            if 'http:' in label_text[i]:
                update_icon_label(label, text)
            else:
                update_label(label, text)
                
        # self.update_label(self.weather_labels[0], "Today's Weather")
        # self.update_icon_label(self.weather_labels[1], f"http:{current_weather['condition']['icon']}", "current_weather_icon.png")
        # self.update_label(self.weather_labels[2], f"Current Condition: {current_weather['condition']['text']}")
        # self.update_label(self.weather_labels[3], f"Current Wind: {current_weather['wind_mph']}mph | {current_weather['wind_kph']}kph {current_weather['wind_dir']}")
        # self.update_label(self.weather_labels[4], f"Current Humidity: {current_weather['humidity']}%")

        # self.update_icon_label(self.weather_labels[5], f"http:{forecast_weather['condition']['icon']}", "forecast_weather_icon.png")
        # self.update_label(self.weather_labels[6], f"Max Temperature: {forecast_weather['maxtemp_f']}°F | {forecast_weather['maxtemp_c']}°C")
        # self.update_label(self.weather_labels[7], f"Min Temperature: {forecast_weather['mintemp_f']}°F | {forecast_weather['maxtemp_c']}°C")
        # self.update_label(self.weather_labels[8], f"Max Wind: {forecast_weather['maxwind_mph']}mph | {forecast_weather['maxwind_kph']}kph")
        # self.update_label(self.weather_labels[9], f"Average Humidity: {forecast_weather['avghumidity']}%")
        # self.update_label(self.weather_labels[10], f"Chance of Rain: {forecast_weather['daily_chance_of_rain']}%")

    def update_label(self, label, text):
        label.config(text=text)

    def update_icon_label(self, label, icon_url): # *Please check if this function is working as intended
        self.download_icon(icon_url, "icon.png")
        icon = ImageTk.PhotoImage(file = "icon.png")
        self.label.config(image = icon)
        self.label.image = icon

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

if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()