# Weather App

The Weather App is a simple Python application that provides weather information for a specified location. It uses the tkinter library for the graphical user interface (GUI) and fetches weather data from the WeatherAPI. The app displays both current weather conditions and a 7-day weather forecast.

## Features

- Display current weather conditions, including temperature, wind speed, humidity, and weather icon.
- View a 7-day weather forecast with maximum and minimum temperatures.
- Click on a forecast day to see detailed weather information for that day.
- Easily switch between different locations by entering the city, state, or country in the input field.

## Requirements

- Python 3.x
- tkinter library
- PIL (Pillow) library
- requests library

## Setup

1. Clone the repository to your local machine:
```shell
git clone https://github.com/your-username/weather-app.git
```

2. Navigate to the project directory:
```shell
cd weather-app
```

3. Install the required Python packages:
```shell
pip install -r requirements.txt
```

4. Get an API key from WeatherAPI and replace "YOUR_API_KEY" in ui.py with your actual API key.

## Usage

1. Run the application using the following command:
```shell
python weather_app.py
```

2. The Weather App GUI will open.

3. Enter the location (e.g., "New York, NY") in the input field.

4. Click the "Get Weather" button or press Enter to fetch weather data.

5. The current weather conditions and 7-day forecast will be displayed.

6. Click on a forecast day to view detailed weather information for that day.

7. Enjoy exploring the weather!
