import json
import requests
from datetime import datetime, timedelta
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

API_KEY = "04cefdc70dc64f37bf001213232309"
N_DAYS_FORECAST = 8 # Make this into a 7 day forecast - Karan

class WeatherApp(Tk):
    """A simple weather application using Tkinter for the GUI."""

    def __init__(self):
        """Initialize the WeatherApp class."""
        super().__init__()
        self.title("Weather App")
        self.geometry("1500x500")
        self.create_widgets()

    def create_widgets(self):
        """Create GUI widgets and layout for the WeatherApp."""
        Label(self, text="Enter City, State or Country: ").grid(row = 0, column = 0, sticky="nsew")
        self.location_entry = Entry(self, width = 20)
        self.location_entry.grid(row = 0, column = 1, sticky="nsew")
        Button(self, text = "Get Weather", command = self.get_weather).grid(row = 0, column = 2, sticky = "nsew")


        ##### This is the popup menu for forecast day selection ######
        #self.n = StringVar()
        #self.n.trace('w', self.get_forecast_change) #This is for detecting a change in popup menu
        #self.forecast_day_chooser = ttk.Combobox(self, width = 18, textvariable = self.n)
        #self.forecast_day_chooser["values"] = self.create_forecast_options()
        #self.forecast_day_chooser.grid(column = 0, row = 1, sticky="nsew")
        #self.forecast_day_chooser.current(0)
        ##############################################################

        self.weather_labels = []
        self.create_weather_labels(row = 2, column = 0, columnspan = 1)

    def get_forecast_change(self, index, value, op): # what is the purpose for passing values - Karan
        """
        Callback for handling forecast day changes in the popup menu.

        Reloads the weather data when the forecast day is changed.

        Args:
            index (int): The index of the selected day.
            value (str): The value of the selected day.
            op (str): The type of operation (unused).
        """
        if self.location_entry.get(): #setting the current value triggers the change, so we check to make sure there's a location
            self.get_weather()

    def create_forecast_options(self): # The naming can be better instead of mentioning days, mention the date instead - Karan
        """
        Create forecast options for the popup menu.

        Generates a list of day names for future forecast days.

        Returns:
            tuple: A tuple of forecast day options.
        """
        try:
            dt = datetime.now()
            day_chooser_values = [" Today's Forecast", " Tomorrow's Forecast"]
            dt += timedelta(days = 1)
            for i in range( 2, N_DAYS_FORECAST ):
                dt += timedelta(days = 1)
                if i >= 7:  #if it's a week away or more
                    day_chooser_values.append(f" Next {dt.strftime('%A')}'s Forecast") # say "next day"
                else:
                    day_chooser_values.append(f" {dt.strftime('%A')}'s Forecast") # otherwise just day
            return tuple(day_chooser_values)
        except Exception as e:
            messagebox.showerror("Error", f"Error creating forecast options: {e}")

    def create_weather_labels(self, row, column, columnspan):
        """
        Create and layout weather labels.

        Args:
            row (int): The starting row for labels.
            column (int): The starting column for labels.
            columnspan (int): The number of columns each label spans.
        """
        labels = [ # List of dictionaries of labels with its respective values
            {"current_label" : "", # current label
            "row" : row, "column" : column, "columnspan" : columnspan},

            {"current_weather_icon" : "", # current weather icon
            "row" : row + 1, "column" : column, "columnspan" : columnspan},

            {"current_condition" : "", # current condition
            "row" : row + 2,  "column" : column, "columnspan" : columnspan},

            {"current_temperature" : "", # current temperature
            "row" : row + 3,  "column" : column, "columnspan" : columnspan},

            {"current_wind_speed" : "", # current wind speed
            "row" : row + 4,  "column" : column, "columnspan" : columnspan},

            {"current_humidity" : "", # current humidity
            "row" : row + 5,  "column" : column, "columnspan" : columnspan},

            {"spacer_1" : "", # Spacer label to create a gap between today's cast and forecast
            "row" : row + 6,  "column" : column, "columnspan" : columnspan},

            {"forecast_day" : "", # Forecast label
            "row" : row + 7,  "column" : column, "columnspan" : columnspan},

            {"forecast_icon" : "", # forecast icon
            "row" : row + 8,  "column" : column, "columnspan" : columnspan},

            {"forecast_condition" : "", # forecast condition
            "row" : row + 9,  "column" : column, "columnspan" : columnspan},

            {"forecast_max_temperature" : "", # forecast max temperature
            "row" : row + 10,  "column" : column, "columnspan" : columnspan},

            {"forecast_min_temperature" : "", # forecast min temperature
            "row" : row + 11, "column" : column, "columnspan" : columnspan},

            {"forecast_max_wind_speed" : "", # forecast wind speed
            "row" : row + 12, "column" : column, "columnspan" : columnspan},

            {"forecast_avg_humidity" : "", # forecast humidity
            "row" : row + 13, "column" : column, "columnspan" : columnspan},

            {"forecast_rain_chance" : "", # forecast rain chance
            "row" : row + 14, "column" : column, "columnspan" : columnspan},

            {"forecast_total_precipitation" : "", # forecast total precipitation
            "row" : row + 15, "column" : column, "columnspan" : columnspan},

            {"forecast_day_2" : "", # Forecast label
            "row" : row + 7,  "column" : column + 1, "columnspan" : columnspan},

            {"forecast_icon_2" : "", # forecast icon
            "row" : row + 8,  "column" : column + 1, "columnspan" : columnspan},

            {"forecast_condition_2" : "", # forecast condition
            "row" : row + 9,  "column" : column + 1, "columnspan" : columnspan},

            {"forecast_max_temperature_2" : "", # forecast max temperature
            "row" : row + 10,  "column" : column + 1, "columnspan" : columnspan},

            {"forecast_min_temperature_2" : "", # forecast min temperature
            "row" : row + 11, "column" : column + 1, "columnspan" : columnspan},

            {"forecast_max_wind_speed_2" : "", # forecast wind speed
            "row" : row + 12, "column" : column + 1, "columnspan" : columnspan},

            {"forecast_avg_humidity_2" : "", # forecast humidity
            "row" : row + 13, "column" : column + 1, "columnspan" : columnspan},

            {"forecast_rain_chance_2" : "", # forecast rain chance
            "row" : row + 14, "column" : column + 1, "columnspan" : columnspan},

            {"forecast_total_precipitation_2" : "", # forecast total precipitation
            "row" : row + 15, "column" : column + 1, "columnspan" : columnspan},

            {"forecast_day_3" : "", # Forecast label
            "row" : row + 7,  "column" : column + 2, "columnspan" : columnspan},

            {"forecast_icon_3" : "", # forecast icon
            "row" : row + 8,  "column" : column + 2, "columnspan" : columnspan},

            {"forecast_condition_3" : "", # forecast condition
            "row" : row + 9,  "column" : column + 2, "columnspan" : columnspan},

            {"forecast_max_temperature_3" : "", # forecast max temperature
            "row" : row + 10,  "column" : column + 2, "columnspan" : columnspan},

            {"forecast_min_temperature_3" : "", # forecast min temperature
            "row" : row + 11, "column" : column + 2, "columnspan" : columnspan},

            {"forecast_max_wind_speed_3" : "", # forecast wind speed
            "row" : row + 12, "column" : column + 2, "columnspan" : columnspan},

            {"forecast_avg_humidity_3" : "", # forecast humidity
            "row" : row + 13, "column" : column + 2, "columnspan" : columnspan},

            {"forecast_rain_chance_3" : "", # forecast rain chance
            "row" : row + 14, "column" : column + 2, "columnspan" : columnspan},

            {"forecast_total_precipitation_3" : "", # forecast total precipitation
            "row" : row + 15, "column" : column + 2, "columnspan" : columnspan},

            {"forecast_day_4" : "", # Forecast label
            "row" : row + 7,  "column" : column + 18, "columnspan" : columnspan},

            {"forecast_icon_4" : "", # forecast icon
            "row" : row + 8,  "column" : column + 18, "columnspan" : columnspan},

            {"forecast_condition_4" : "", # forecast condition
            "row" : row + 9,  "column" : column + 18, "columnspan" : columnspan},

            {"forecast_max_temperature_4" : "", # forecast max temperature
            "row" : row + 10,  "column" : column + 18, "columnspan" : columnspan},

            {"forecast_min_temperature_4" : "", # forecast min temperature
            "row" : row + 11, "column" : column + 18, "columnspan" : columnspan},

            {"forecast_max_wind_speed_4" : "", # forecast wind speed
            "row" : row + 12, "column" : column + 18, "columnspan" : columnspan},

            {"forecast_avg_humidity_4" : "", # forecast humidity
            "row" : row + 13, "column" : column + 18, "columnspan" : columnspan},

            {"forecast_rain_chance_4" : "", # forecast rain chance
            "row" : row + 14, "column" : column + 18, "columnspan" : columnspan},

            {"forecast_total_precipitation_4" : "", # forecast total precipitation
            "row" : row + 15, "column" : column + 18, "columnspan" : columnspan},

            {"forecast_day_5" : "", # Forecast label
            "row" : row + 7,  "column" : column + 33, "columnspan" : columnspan},

            {"forecast_icon_5" : "", # forecast icon
            "row" : row + 8,  "column" : column + 33, "columnspan" : columnspan},

            {"forecast_condition_5" : "", # forecast condition
            "row" : row + 9,  "column" : column + 33, "columnspan" : columnspan},

            {"forecast_max_temperature_5" : "", # forecast max temperature
            "row" : row + 10,  "column" : column + 33, "columnspan" : columnspan},

            {"forecast_min_temperature_5" : "", # forecast min temperature
            "row" : row + 11, "column" : column + 33, "columnspan" : columnspan},

            {"forecast_max_wind_speed_5" : "", # forecast wind speed
            "row" : row + 12, "column" : column + 33, "columnspan" : columnspan},

            {"forecast_avg_humidity_5" : "", # forecast humidity
            "row" : row + 13, "column" : column + 33, "columnspan" : columnspan},

            {"forecast_rain_chance_5" : "", # forecast rain chance
            "row" : row + 14, "column" : column + 33, "columnspan" : columnspan},

            {"forecast_total_precipitation_5" : "", # forecast total precipitation
            "row" : row + 15, "column" : column + 33, "columnspan" : columnspan},

            {"forecast_day_6" : "", # Forecast label
            "row" : row + 7,  "column" : column + 48, "columnspan" : columnspan},

            {"forecast_icon_6" : "", # forecast icon
            "row" : row + 8,  "column" : column + 48, "columnspan" : columnspan},

            {"forecast_condition_6" : "", # forecast condition
            "row" : row + 9,  "column" : column + 48, "columnspan" : columnspan},

            {"forecast_max_temperature_6" : "", # forecast max temperature
            "row" : row + 10,  "column" : column + 48, "columnspan" : columnspan},

            {"forecast_min_temperature_6" : "", # forecast min temperature
            "row" : row + 11, "column" : column + 48, "columnspan" : columnspan},

            {"forecast_max_wind_speed_6" : "", # forecast wind speed
            "row" : row + 12, "column" : column + 48, "columnspan" : columnspan},

            {"forecast_avg_humidity_6" : "", # forecast humidity
            "row" : row + 13, "column" : column + 48, "columnspan" : columnspan},

            {"forecast_rain_chance_6" : "", # forecast rain chance
            "row" : row + 14, "column" : column + 48, "columnspan" : columnspan},

            {"forecast_total_precipitation_6" : "", # forecast total precipitation
            "row" : row + 15, "column" : column + 48, "columnspan" : columnspan},

            {"forecast_day_7" : "", # Forecast label
            "row" : row + 7,  "column" : column + 63, "columnspan" : columnspan},

            {"forecast_icon_7" : "", # forecast icon
            "row" : row + 8,  "column" : column + 63, "columnspan" : columnspan},

            {"forecast_condition_7" : "", # forecast condition
            "row" : row + 9,  "column" : column + 63, "columnspan" : columnspan},

            {"forecast_max_temperature_7" : "", # forecast max temperature
            "row" : row + 10,  "column" : column + 63, "columnspan" : columnspan},

            {"forecast_min_temperature_7" : "", # forecast min temperature
            "row" : row + 11, "column" : column + 63, "columnspan" : columnspan},

            {"forecast_max_wind_speed_7" : "", # forecast wind speed
            "row" : row + 12, "column" : column + 63, "columnspan" : columnspan},

            {"forecast_avg_humidity_7" : "", # forecast humidity
            "row" : row + 13, "column" : column + 63, "columnspan" : columnspan},

            {"forecast_rain_chance_7" : "", # forecast rain chance
            "row" : row + 14, "column" : column + 63, "columnspan" : columnspan},

            {"forecast_total_precipitation_7" : "", # forecast total precipitation
            "row" : row + 15, "column" : column + 63, "columnspan" : columnspan},

            {"forecast_day_8" : "", # Forecast label
            "row" : row + 7,  "column" : column + 78, "columnspan" : columnspan},

            {"forecast_icon_8" : "", # forecast icon
            "row" : row + 8,  "column" : column + 78, "columnspan" : columnspan},

            {"forecast_condition_8" : "", # forecast condition
            "row" : row + 9,  "column" : column + 78, "columnspan" : columnspan},

            {"forecast_max_temperature_8" : "", # forecast max temperature
            "row" : row + 10,  "column" : column + 78, "columnspan" : columnspan},

            {"forecast_min_temperature_8" : "", # forecast min temperature
            "row" : row + 11, "column" : column + 78, "columnspan" : columnspan},

            {"forecast_max_wind_speed_8" : "", # forecast wind speed
            "row" : row + 12, "column" : column + 78, "columnspan" : columnspan},

            {"forecast_avg_humidity_8" : "", # forecast humidity
            "row" : row + 13, "column" : column + 78, "columnspan" : columnspan},

            {"forecast_rain_chance_8" : "", # forecast rain chance
            "row" : row + 14, "column" : column + 78, "columnspan" : columnspan},

            {"forecast_total_precipitation_8" : "", # forecast total precipitation
            "row" : row + 15, "column" : column + 78, "columnspan" : columnspan},
        ]

        for label_info in labels:
            label_name = list(label_info.keys())[0]
            label_text = label_info[label_name]
            label_row = label_info["row"]
            label_column = label_info["column"]
            label_columnspan = label_info["columnspan"]

            label = Label(self, text = label_text)
            label.grid(row = label_row, column = label_column, columnspan = label_columnspan, sticky = "nsew")
            print(f"{label_name} : {label}")
            self.weather_labels.append({label_name : label})

    def get_weather(self):
        """Get weather data and update the GUI."""
        try:
            location = self.location_entry.get()

            if not location:
                raise ValueError("Location Cannot be empty!")

            weather_data = WeatherData(API_KEY, N_DAYS_FORECAST, location)
            weather_data.fetch_data(0)

            current_weather = weather_data.get_current_weather()
            forecast_weather = weather_data.get_forecast_weather(0)
            forecast_weather_list = []
            for n in range(1, N_DAYS_FORECAST):
                forecast_weather_list.append(weather_data.get_forecast_weather(n))

            self.update_all_labels(current_weather, forecast_weather, forecast_weather_list)
        except ValueError as e:
            raise e
            #messagebox.showerror("Error", f"{e}")
        except Exception as e:
            raise e
            #messagebox.showerror("Error", f"Error geting weather: {e}")


    def update_all_labels(self, current_weather, forecast_weather, forecast_weather_list):
        """
        Update all weather labels with new data.

        Args:
            current_weather (dict): Current weather data.
            forecast_weather (dict): Forecasted weather data.
        """
        label_commands = [
            {"current_label"                : f"Current Weather\n as of {current_weather['last_updated']}"},
            {"current_weather_icon"         : f"http:{current_weather['condition']['icon']}"},
            {"current_condition"            : f"Conditions: {current_weather['condition']['text']}"},
            {"current_temperature"          : f"Temperature: {current_weather['temp_f']}°F | {current_weather['temp_c']}°C"},
            {"current_wind_speed"           : f"Wind: {current_weather['wind_mph']}mph | {current_weather['wind_kph']}kph {current_weather['wind_dir']}"},
            {"current_humidity"             : f"Humidity: {current_weather['humidity']}%"},
            {"spacer_1"                     : f" "},
            {"forecast_day"                 : f"Today's Forecast"},
            {"forecast_icon"                : f"http:{forecast_weather['condition']['icon']}"},
            {"forecast_condition"           : f"Conditions: {forecast_weather['condition']['text']}"},
            {"forecast_max_temperature"     : f"Max Temp: {forecast_weather['maxtemp_f']}°F | {forecast_weather['maxtemp_c']}°C"},
            {"forecast_min_temperature"     : f"Min Temp: {forecast_weather['mintemp_f']}°F | {forecast_weather['mintemp_c']}°C"},
            {"forecast_max_wind_speed"      : f"Max Wind: {forecast_weather['maxwind_mph']}mph | {forecast_weather['maxwind_kph']}kph"},
            {"forecast_avg_humidity"        : f"Avg Humidity: {forecast_weather['avghumidity']}%"},
            {"forecast_rain_chance"         : f"Chance of Rain: {forecast_weather['daily_chance_of_rain']}%"},
            {"forecast_total_precipitation" : f"Total Precip.: {forecast_weather['totalprecip_in']}in | {forecast_weather['totalprecip_mm']}mm"}
        ]

        for day in range(0, N_DAYS_FORECAST - 1):
            label_commands.append({f"forecast_day_{day + 2}"                 : f"{self.create_forecast_options()[day+1]}"})
            label_commands.append({f"forecast_icon_{day + 2}"                : f"http:{forecast_weather_list[day]['condition']['icon']}"})
            label_commands.append({f"forecast_condition_{day + 2}"           : f"Conditions: {forecast_weather_list[day]['condition']['text']}"})
            label_commands.append({f"forecast_max_temperature_{day + 2}"     : f"Max Temp: {forecast_weather_list[day]['maxtemp_f']}°F | {forecast_weather_list[day]['maxtemp_c']}°C"})
            label_commands.append({f"forecast_min_temperature_{day + 2}"     : f"Min Temp: {forecast_weather_list[day]['mintemp_f']}°F | {forecast_weather_list[day]['mintemp_c']}°C"})
            label_commands.append({f"forecast_max_wind_speed_{day + 2}"      : f"Max Wind: {forecast_weather_list[day]['maxwind_mph']}mph | {forecast_weather_list[day]['maxwind_kph']}kph"})
            label_commands.append({f"forecast_avg_humidity_{day + 2}"        : f"Avg Humidity: {forecast_weather_list[day]['avghumidity']}%"})
            label_commands.append({f"forecast_rain_chance_{day + 2}"         : f"Chance of Rain: {forecast_weather_list[day]['daily_chance_of_rain']}%"})
            label_commands.append({f"forecast_total_precipitation_{day + 2}" : f"Total Precip.: {forecast_weather_list[day]['totalprecip_in']}in | {forecast_weather_list[day]['totalprecip_mm']}mm"})

        for label_info, update_command in zip(self.weather_labels, label_commands):
            label_name = list(label_info.keys())[0]
            label = label_info[label_name]
            update_command = update_command[label_name]

            if "http:" in update_command:
                self.update_icon_label(label, update_command)
            else:
                self.update_label(label, update_command)

    def update_label(self, label, text):
        """
        Update a label's text.

        Args:
            label (Label): The label widget to update.
            text (str): The new text for the label.
        """
        label.config(text = text)

    def update_icon_label(self, label, icon_url):
        """
        Update a label with an icon image from a URL.

        Args:
            label (Label): The label widget to update with an icon.
            icon_url (str): The URL of the icon image.
        """
        self.download_icon(icon_url, "temp_icon.png")
        icon = ImageTk.PhotoImage(file = "temp_icon.png")
        label.config(image = icon)
        label.image = icon

    def download_icon(self, url, filename):
        """
        Download an icon image from a URL.

        Args:
            url (str): The URL of the icon image to download.
            filename (str): The name of the file to save the icon.
        """
        try:
            response = requests.get(url, stream = True)
            if response.status_code == 200:
                with open(filename, "wb") as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
            else:
                raise ValueError(f"Icon download request failed with status code {response.status_code}")
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred downloading icon: {e}")

class WeatherData:
    """Class to fetch weather data using an API."""

    def __init__(self, API_KEY, N_DAYS_FORECAST, location):
        """
        Initialize the WeatherData class.

        Args:
            API_KEY (str): The API key for weather data.
            N_DAYS_FORECAST (int): The number of days to forecast.
            location (str): The location for weather data retrieval.
        """
        self.API_KEY = API_KEY
        self.N_DAYS_FORECAST = N_DAYS_FORECAST
        self.location = location
        self.weather_data = []
        self.current_weather = []
        self.forecast_weather = []

    def fetch_data(self, day):
        """
        Fetch weather data from the API and store it.

        Args:
            day (int): The index of the selected forecast day.
        """
        try:
            url = f"http://api.weatherapi.com/v1/forecast.json?key={self.API_KEY}&q={self.location}&days={self.N_DAYS_FORECAST}&aqi=no&alerts=no"
            response = requests.get(url)
            if response.status_code == 200:
                self.weather_data = json.loads(response.content)
                self.current_weather = self.weather_data["current"]
                self.forecast_weather = self.weather_data["forecast"]["forecastday"][day]["day"]
            else:
                raise Exception(f"API request failed with status code {response.status_code}")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching weather data: {e}")

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
        return self.weather_data["forecast"]["forecastday"][day]["day"]

if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()
