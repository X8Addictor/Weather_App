class WeatherAppError(Exception):
    """Custom exception class for the Weather App."""
    def __init__(self, message):
        super().__init__(message)