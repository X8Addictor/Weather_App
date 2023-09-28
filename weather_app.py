from tkinter import *
from ui import WeatherAppUI

# Starting point of the application
if __name__ == "__main__":
    root = Tk()
    app_ui = WeatherAppUI(root)
    app_ui.run()
