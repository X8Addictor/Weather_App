import json, requests
from datetime import datetime, timedelta
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

API_KEY = "04cefdc70dc64f37bf001213232309"
N_DAYS_FORECAST = 10

class App(Tk):
    def __init__(self):
        super().__init__()

def retrieve_weather_data(location):
    data = requests.get(f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={location}&days={N_DAYS_FORECAST}&aqi=no&alerts=no")
    if data.status_code == 200:
        return json.loads(data.content)
    else:
        print("Was not able to download weather data.")

def download_icon(url):
    try:
        r = requests.get(url, stream = True)
        if r.status_code == 200:
            with open("icon.png", "wb") as f:
                for chunk in r:
                    f.write(chunk)
    except Exception as e:
        print(f"Error ocurred downloading icon: {e}")

def download_forecast_icon(url):
    try:
        r = requests.get(url, stream = True)
        if r.status_code == 200:
            with open("fore_icon.png", "wb") as f:
                for chunk in r:
                    f.write(chunk)
    except Exception as e:
        print(f"Error ocurred downloading icon: {e}")

def get_forecast_change(index, value, op):
    get_weather_clicked()

def get_weather_clicked():
    if loc_txt.get() != "":
        weather = retrieve_weather_data(loc_txt.get())

        current_weather = weather["current"]

        today_lbl.configure(text = f"Today's Weather as of {current_weather['last_updated']}")
        temp_lbl.configure(text = f"Current Temperature: {current_weather['temp_f']} deg F")
        cond_lbl.configure(text = f"Current Condition: {current_weather['condition']['text']}")
        wind_lbl.configure(text = f"Current Wind: {current_weather['wind_mph']}mph {current_weather['wind_dir']}")
        humid_lbl.configure(text = f"Current Humidity: {current_weather['humidity']}%")

        download_icon(f"http:{current_weather['condition']['icon']}")
        img = ImageTk.PhotoImage(file = "icon.png")
        img_panel = Label(app, image = img)
        img_panel.image = img
        img_panel.grid(column = 1, row = 2)

        forecast_weather = weather["forecast"]["forecastday"][forecast_day_chooser.current()]["day"]

        fore_cond_lbl.configure(text = f"Forecast Condition: {forecast_weather['condition']['text']}")
        max_temp_lbl.configure(text = f"Max Temperature: {forecast_weather['maxtemp_f']} deg F")
        min_temp_lbl.configure(text = f"Min Temperature: {forecast_weather['mintemp_f']} deg F")
        fore_wind_lbl.configure(text = f"Max Wind: {forecast_weather['maxwind_mph']}mph")
        avg_humid_lbl.configure(text = f"Avg Humidity: {forecast_weather['avghumidity']}%")
        chance_rain_lbl.configure(text = f"Chance of Rain: {forecast_weather['daily_chance_of_rain']}%")

        download_forecast_icon(f"http:{forecast_weather['condition']['icon']}")
        fore_img = ImageTk.PhotoImage(file = "fore_icon.png")
        fore_img_panel = Label(app, image = fore_img)
        fore_img_panel.image = fore_img
        fore_img_panel.grid(column = 1, row = 8)

if __name__ == "__main__":
    app = App()
    app.title("Weather App")
    app.geometry("640x480")

    entry_lbl = Label(app, text = "Enter City, State (or Country): ")
    entry_lbl.grid()

    loc_txt = Entry(app, width = 20)
    loc_txt.grid(column = 1, row = 0)

    btn = Button(app, text = "Get Weather", command = get_weather_clicked)
    btn.grid(column = 2, row = 0)

    today_lbl = Label(app, text = "")
    today_lbl.grid(column = 1, row = 1)

    cond_lbl = Label(app, text = "")
    cond_lbl.grid(column = 1, row = 3)
    temp_lbl = Label(app, text = "")
    temp_lbl.grid(column = 1, row = 4)
    wind_lbl = Label(app, text = "")
    wind_lbl.grid(column = 1, row = 5)
    humid_lbl = Label(app, text = "")
    humid_lbl.grid(column = 1, row = 6)

    #separator_lbl = Label(app, text = " ")
    #separator_lbl.grid(column = 1, row = 7)
    n = StringVar()
    n.trace('w',get_forecast_change)
    forecast_day_chooser = ttk.Combobox(app, width = 15, textvariable = n)
    dt = datetime.now()
    day_chooser_values = [" Today's Forecast", " Tomorrow's Forecast"]
    dt += timedelta(days = 1)
    for i in range(2,10):
        dt += timedelta(days = 1)
        if i >= 7:
            day_chooser_values.append(f" Next {dt.strftime('%A')}'s Forecast")
        else:
            day_chooser_values.append(f" {dt.strftime('%A')}'s Forecast")

    forecast_day_chooser["values"] = tuple(day_chooser_values)
    forecast_day_chooser.grid(column = 1, row = 7)
    forecast_day_chooser.current(0)

    fore_cond_lbl = Label(app, text = "")
    fore_cond_lbl.grid(column = 1, row = 9)
    max_temp_lbl = Label(app, text = "")
    max_temp_lbl.grid(column = 1, row = 10)
    min_temp_lbl = Label(app, text = "")
    min_temp_lbl.grid(column = 1, row = 11)
    fore_wind_lbl = Label(app, text = "")
    fore_wind_lbl.grid(column = 1, row = 12)
    avg_humid_lbl = Label(app, text = "")
    avg_humid_lbl.grid(column = 1, row = 13)
    chance_rain_lbl = Label(app, text = "")
    chance_rain_lbl.grid(column = 1, row = 14)

    app.mainloop()
