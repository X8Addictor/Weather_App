from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from weather_data import WeatherData
from datetime import datetime, timedelta
from weather_exception import WeatherAppError
import requests

# Constants for weather data
API_KEY = "04cefdc70dc64f37bf001213232309"
N_DAYS_FORECAST = 8

# Constants for color
BACKGROUND_COLOR = "#0096FF"
LIGHT_BG_COLOR = "#88cffa"
MAX_TEMP_COLOR = "#942211"
MIN_TEMP_COLOR = "Blue"
FORECAST_COLOR = "White"
CURRENT_WEATHER_COLOR = "White"
DEFAULT_TEXT_COLOR = "White"

class WeatherAppUI:
    """A simple weather application using Tkinter for the GUI."""

    def __init__(self, root):
        """
        Initialize the WeatherApp class.

        Creates the main application window and sets up the initial UI.
        """
        super().__init__()
        self.root = root
        self.root.configure(bg = BACKGROUND_COLOR)
        self.root.title("Weather App")
        self.root.geometry("900x1100")
        self.weather_labels = []
        self.detailed_forecast_labels = []
        self.forecast_frames = []
        self.create_widgets()

    def create_widgets(self):
        """Create GUI widgets and layout for the WeatherApp."""
        self.create_input_section()
        self.create_current_labels(row = 2, column = 0, rowspan = 1, columnspan = 1)
        self.create_forecast_labels(row = 3, column = 0, rowspan = 1, columnspan = 1)
        self.create_detailed_forecast_labels(row = 2, column = 0, rowspan = 1, columnspan = 1)

    def create_input_section(self):
        """
        Create and layout input section.

        This section includes a label, an entry field, and a "Get Weather" button.
        """
        Label(self.root, text="Enter City, State or Country: ").grid(row = 0, column = 0, sticky = "nsew")
        self.location_entry = Entry(self.root, width = 20)
        self.location_entry.grid(row = 0, column = 1, sticky = "nsew")
        self.location_entry.bind('<Return>', self.get_weather)
        self.location_entry.focus_set()
        Button(self.root, text = "Get Weather", command = self.get_weather).grid(row = 0, column = 2, sticky = "nsew")

    def create_current_labels(self, row, column, rowspan, columnspan):
        """
        Create and layout the current weather labels.

        Args:
            row (int): The starting row for the current weather labels.
            column (int): The starting column for the current weather labels.
            rowspan (int): The number of rows the current weather section spans.
            columnspan (int): The number of columns the current weather section spans.

        This function creates a frame to display the current weather information, including labels for weather conditions,
        temperature, wind speed, and humidity. The labels are placed within the specified grid layout.
        """
        current_weather_frame = Frame(self.root)
        current_weather_frame.config(bg = BACKGROUND_COLOR)
        current_weather_frame.grid(row = row, column = column, rowspan = rowspan, columnspan = columnspan + 1, sticky = "nsew")

        labels = [ # List of current weather labels with its respective grid values
            {"current_label"        : "", "row": 0, "column": 0, "rowspan": rowspan,     "columnspan": columnspan + 1},
            {"current_weather_icon" : "", "row": 1, "column": 0, "rowspan": rowspan + 4, "columnspan": columnspan},
            {"current_condition"    : "", "row": 1, "column": 1, "rowspan": rowspan,     "columnspan": columnspan},
            {"current_temperature"  : "", "row": 2, "column": 1, "rowspan": rowspan,     "columnspan": columnspan},
            {"current_wind_speed"   : "", "row": 3, "column": 1, "rowspan": rowspan,     "columnspan": columnspan},
            {"current_humidity"     : "", "row": 4, "column": 1, "rowspan": rowspan,     "columnspan": columnspan},
        ]

        self.create_labels(labels, current_weather_frame)
        self.forecast_frames.append(current_weather_frame)

    def create_forecast_labels(self, row, column, rowspan, columnspan):
        """
        Create and layout forecast weather labels.

        Args:
            row (int): The starting row for labels.
            column (int): The starting column for labels.
            rowspan (int): The number of rows each label spans
            columnspan (int): The number of columns each label spans.

        This function creates a frame to display the forecast weather information, including labels for weather conditions,
        temperature, wind speed, and humidity. The labels are placed within the specified grid layout. 
        Each frame is then binded with mouse button one for event handling.
        """
        for day in range(N_DAYS_FORECAST):
            forecast_frame = Frame(self.root)
            forecast_frame.config(bg=BACKGROUND_COLOR)
            forecast_frame.grid(row = row + day * 8, column = column, rowspan = rowspan, columnspan = columnspan + 1, sticky="nsew")

            labels = [ # List of forecast labels with its respective grid values
                {f"forecast_day_{day + 1}"             : "", "row" : 0, "column": 0, "rowspan": rowspan,     "columnspan": columnspan + 1},
                {f"forecast_icon_{day + 1}"            : "", "row" : 1, "column": 0, "rowspan": rowspan + 2, "columnspan": columnspan},
                {f"forecast_max_temperature_{day + 1}" : "", "row" : 1, "column": 1, "rowspan": rowspan,     "columnspan": columnspan},
                {f"forecast_min_temperature_{day + 1}" : "", "row" : 2, "column": 1, "rowspan": rowspan,     "columnspan": columnspan},
            ]

            self.create_labels(labels, forecast_frame)
            forecast_frame.bind("<Button-1>", lambda event, frame = forecast_frame: self.update_detailed_forecast(frame))
            self.forecast_frames.append(forecast_frame)

    def create_detailed_forecast_labels(self, row, column, rowspan, columnspan):
        """
        Create and layout detailed forecast labels.

        Args:
            row (int): The starting row for the detailed forecast labels.
            column (int): The starting column for the detailed forecast labels.
            rowspan (int): The number of rows the detailed forecast section spans.
            columnspan (int): The number of columns the detailed forecast section spans.

        This function creates a frame to display detailed forecast information, including labels for day, weather conditions,
        temperature, wind speed, humidity, rain chance, and total precipitation. The labels are placed within the specified
        grid layout.
        """
        detailed_forecast_frame = Frame(self.root)
        detailed_forecast_frame.config(bg = BACKGROUND_COLOR)
        detailed_forecast_frame.grid(row = row, column = column + 3, rowspan = rowspan + 1, columnspan = columnspan + 2, sticky = "nsew")

        labels = [ # List of detailed forecast labels with its respective grid values
            {"detailed_forecast_day"                 : "", "row" : row,     "column" : column + 10, "rowspan" : rowspan, "columnspan" : columnspan},
            {"detailed_forecast_icon"                : "", "row" : row + 1, "column" : column + 10, "rowspan" : rowspan, "columnspan" : columnspan},
            {"detailed_forecast_condition"           : "", "row" : row + 2, "column" : column + 10, "rowspan" : rowspan, "columnspan" : columnspan},
            {"detailed_forecast_max_temperature"     : "", "row" : row + 3, "column" : column + 10, "rowspan" : rowspan, "columnspan" : columnspan},
            {"detailed_forecast_min_temperature"     : "", "row" : row + 4, "column" : column + 10, "rowspan" : rowspan, "columnspan" : columnspan},
            {"detailed_forecast_max_wind_speed"      : "", "row" : row + 5, "column" : column + 10, "rowspan" : rowspan, "columnspan" : columnspan},
            {"detailed_forecast_avg_humidity"        : "", "row" : row + 6, "column" : column + 10, "rowspan" : rowspan, "columnspan" : columnspan},
            {"detailed_forecast_rain_chance"         : "", "row" : row + 7, "column" : column + 10, "rowspan" : rowspan, "columnspan" : columnspan},
            {"detailed_forecast_total_precipitation" : "", "row" : row + 8, "column" : column + 10, "rowspan" : rowspan, "columnspan" : columnspan},
        ]

        self.create_labels(labels, detailed_forecast_frame)
    
    def create_labels(self, labels, parent_frame):
        """
        Create and layout labels within a parent frame.

        Args:
            labels (list): A list of dictionaries containing label information.
            parent_frame (Frame): The parent frame to place labels in.
        """
        for label_info in labels:
            label_name = list(label_info.keys())[0]
            label_text = label_info[label_name]
            label_row = label_info["row"]
            label_column = label_info["column"]
            label_rowspan = label_info["rowspan"]
            label_columnspan = label_info["columnspan"]

            label = Label(parent_frame, text = label_text, fg = "Black", bg=BACKGROUND_COLOR)
            label.bind("<Button-1>", lambda event, frame = parent_frame: self.update_detailed_forecast(frame)) # Created a lambda function directly within label.bind
            label.grid(row = label_row, column = label_column, rowspan = label_rowspan, columnspan = label_columnspan, sticky = "nsew")

            if "detailed_forecast" in label_name:
                self.detailed_forecast_labels.append({label_name : label})
            else:
                self.weather_labels.append({label_name : label})

    def get_weather(self, *args):
        """Get weather data and update the GUI."""
        try:
            location = self.location_entry.get()

            if not location:
                raise ValueError("Location Cannot be empty!")

            self.weather_data = WeatherData(API_KEY, N_DAYS_FORECAST, location)
            self.weather_data.fetch_data()

            current_weather = self.weather_data.get_current_weather()
            forecast_weather_list = []

            for n in range(0, N_DAYS_FORECAST):
                forecast_weather_list.append(self.weather_data.get_forecast_weather(n))

            self.update_all_labels(current_weather, forecast_weather_list)
        except ValueError as e:
            messagebox.showerror("Error", f"{e}")
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Request error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error geting weather: {e}")

    def update_all_labels(self, current_weather, forecast_weather_list):
        """
        Update all weather labels with current and forecast weather data.

        Args:
            current_weather (dict): Current weather data.
            forecast_weather_list (list of dict): List of forecasted weather data for each day.
        """
        try:
            self.update_current_labels(current_weather)
            self.update_forecast_labels(forecast_weather_list)
        except Exception as e:
            raise WeatherAppError(f"Error updating labels: {e}")

    def update_current_labels(self, current_weather):
        """
        Update labels with current weather data.

        Args:
            current_weather (dict): Current weather data.
        """
        try:
            label_commands = {
                "current_label"        : f"Current Weather\n{current_weather['last_updated']}",
                "current_weather_icon" : f"http:{current_weather['condition']['icon']}",
                "current_condition"    : f"Conditions: {current_weather['condition']['text']}",
                "current_temperature"  : f"Temperature: {current_weather['temp_f']}°F | {current_weather['temp_c']}°C",
                "current_wind_speed"   : f"Wind: {current_weather['wind_mph']} mph | {current_weather['wind_kph']} kmph {current_weather['wind_dir']}",
                "current_humidity"     : f"Humidity: {current_weather['humidity']}%",
            }

            self.update_labels(label_commands, self.weather_labels)
        except Exception as e:
            raise WeatherAppError(f"Error updating current labels: {e}")

    def update_forecast_labels(self, forecast_weather_list):
        """
        Update labels with forecasted weather data.

        Args:
            forecast_weather_list (list of dict): List of forecasted weather data for each day.
        """
        try:
            label_commands = {}
            for day in range(0, N_DAYS_FORECAST - 1):
                label_commands.update(self.get_forecast_label_commands(day, forecast_weather_list[day]))
            self.update_labels(label_commands, self.weather_labels)
        except Exception as e:
            raise WeatherAppError(f"Error updating forecast labels: {e}")

    def get_forecast_label_commands(self, day, forecast_weather):
        """
        Generate label commands for a specific forecast day.

        Args:
            day (int): Index of the forecast day.
            forecast_weather (dict): Forecasted weather data for the day.

        Returns:
            dict: Label commands for the forecast day.
        """
        try:
            day_label = f"forecast_day_{day + 1}"
            icon_label = f"forecast_icon_{day + 1}"
            max_temp_label = f"forecast_max_temperature_{day + 1}"
            min_temp_label = f"forecast_min_temperature_{day + 1}"

            return {
                day_label      : f"{self.create_forecast_options()[day]}",
                icon_label     : f"http:{forecast_weather['condition']['icon']}",
                max_temp_label : f"Max Temp: {forecast_weather['maxtemp_f']}°F | {forecast_weather['maxtemp_c']}°C",
                min_temp_label : f"Min Temp: {forecast_weather['mintemp_f']}°F | {forecast_weather['mintemp_c']}°C",
            }
        except Exception as e:
            raise WeatherAppError(f"Error generating forecast label commands: {e}")

    def update_labels(self, label_commands, label_list):
        """
        Update labels based on label commands.

        Args:
            label_commands (dict): Dictionary of label commands.
            label_list (list of dict): List of label dictionaries.
        """
        try:
            for label_name, update_command in label_commands.items():
                label = self.find_label_by_name(label_name, label_list)
                if label and "http:" in update_command:
                    self.update_icon_label(label, update_command)
                elif label and "http:" not in update_command:
                    self.update_label(label, update_command)
        except Exception as e:
            raise WeatherAppError(f"Error updating labels: {e}")

    def find_label_by_name(self, label_name, label_list):
        """
        Find a label by its name in a list of label dictionaries.

        Args:
            label_name (str): The name of the label to find.
            label_list (list of dict): List of label dictionaries.

        Returns:
            Label or None: The label if found, or None if not found.
        """
        try:
            for label_info in label_list:
                if label_name in label_info:
                    return label_info[label_name]
            return None
        except Exception as e:
            raise WeatherAppError(f"Error finding label by name: {e}")

    def create_forecast_options(self):
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
            for i in range(2, N_DAYS_FORECAST):
                dt += timedelta(days = 1)
                if i >= 7:  #if it's a week away or more
                    day_chooser_values.append(f" Next {dt.strftime('%A')}'s Forecast") # say "next day"
                else:
                    day_chooser_values.append(f" {dt.strftime('%A')}'s Forecast") # otherwise just day
            return tuple(day_chooser_values)
        except Exception as e:
            messagebox.showerror("Error", f"Error creating forecast options: {e}")

    def update_detailed_forecast(self, frame):
        """
        Update detailed forecast labels based on the selected frame.

        Args:
            frame (Frame): The frame that was clicked to trigger the update.
        """
        frame_index = self.forecast_frames.index(frame) - 1

        label_commands =  { # List of update commands for detailed forecast weather labels
        "detailed_forecast_day"                 : f"{self.create_forecast_options()[frame_index]} Details",
        "detailed_forecast_icon"                : f"http:{self.weather_data.weather_data['forecast']['forecastday'][frame_index]['day']['condition']['icon']}",
        "detailed_forecast_condition"           : f"Conditions: {self.weather_data.weather_data['forecast']['forecastday'][frame_index]['day']['condition']['text']}",
        "detailed_forecast_max_temperature"     : f"Max Temp: {self.weather_data.weather_data['forecast']['forecastday'][frame_index]['day']['maxtemp_f']}°F | {self.weather_data.weather_data['forecast']['forecastday'][frame_index]['day']['maxtemp_c']}°C",
        "detailed_forecast_min_temperature"     : f"Min Temp: {self.weather_data.weather_data['forecast']['forecastday'][frame_index]['day']['mintemp_f']}°F | {self.weather_data.weather_data['forecast']['forecastday'][frame_index]['day']['mintemp_c']}°C",
        "detailed_forecast_max_wind_speed"      : f"Max Wind: {self.weather_data.weather_data['forecast']['forecastday'][frame_index]['day']['maxwind_mph']} mph | {self.weather_data.weather_data['forecast']['forecastday'][frame_index]['day']['maxwind_kph']} kmph",
        "detailed_forecast_avg_humidity"        : f"Avg Humidity: {self.weather_data.weather_data['forecast']['forecastday'][frame_index]['day']['avghumidity']}%",
        "detailed_forecast_rain_chance"         : f"Chance of Rain: {self.weather_data.weather_data['forecast']['forecastday'][frame_index]['day']['daily_chance_of_rain']}%",
        "detailed_forecast_total_precipitation" : f"Total Precip.: {self.weather_data.weather_data['forecast']['forecastday'][frame_index]['day']['totalprecip_in']}in | {self.weather_data.weather_data['forecast']['forecastday'][frame_index]['day']['totalprecip_mm']}mm"
        }
        
        self.update_labels(label_commands, self.detailed_forecast_labels)

    def update_label(self, label, text):
        """
        Update a label's text.

        Args:
            label (Label): The label widget to update.
            text (str): The new text for the label.
        """
        if "Forecast" in text and "Details" not in text:
            label.config(text = text, bg = BACKGROUND_COLOR, fg = FORECAST_COLOR, font = ("Trebuchet MS", 21, "underline"), anchor = "w")
        elif "Forecast" in text and "Details" in text:
            label.config(text = text, bg = BACKGROUND_COLOR, fg = FORECAST_COLOR, font = ("Trebuchet MS", 21, "underline"), anchor = "center")
        elif "Current Weather" in text:
            label.config(text = text, bg = BACKGROUND_COLOR, fg = CURRENT_WEATHER_COLOR, font = ("Trebuchet MS", 21, "underline"), anchor = "center")
        elif "Min Temp" in text: 
            label.config(text = text, bg = LIGHT_BG_COLOR, fg = MIN_TEMP_COLOR, font = ("Trebuchet MS", 18), anchor = "center")
        elif "Max Temp" in text:
            label.config(text = text, bg = LIGHT_BG_COLOR, fg = MAX_TEMP_COLOR, font = ("Trebuchet MS", 18), anchor = "center")
        else:
            label.config(text = text, bg = BACKGROUND_COLOR, fg = DEFAULT_TEXT_COLOR, font = ("Trebuchet MS", 18), anchor = "center")

    def update_icon_label(self, label, icon_url):
        """
        Update a label with an icon image from a URL.

        Args:
            label (Label): The label widget to update with an icon.
            icon_url (str): The URL of the icon image.
        """
        try:
            self.download_icon(icon_url, "temp_icon.png")
            icon = ImageTk.PhotoImage(file = "temp_icon.png")
            label.config(image = icon)
            label.image = icon
        except WeatherAppError as e:
            messagebox.showerror("Error", f"{e}")
        except IOError as e:
            messagebox.showerror("Error", f"{e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

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
        except requests.RequestException as e:    
            raise WeatherAppError(f"Icon download request failed: {e}")
        except IOError as e:
            raise IOError(f"Error writing icon file: {e}")

    def run(self):
        self.root.mainloop()
