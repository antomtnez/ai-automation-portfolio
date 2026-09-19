import requests
from dotenv import load_dotenv
import os

load_dotenv()

#Test OpenweatherMap
ow_key = os.getenv("OPENWEATHER_API_KEY")
r = requests.get(
    "https://api.openweathermap.org/data/2.5/weather",
    params = {"q" : "Madrid", "appid" : ow_key}
)

print(f"OpenWeatherMap: {r.status_code} - {'Ok' if r.status_code == 200 else 'Error: ' + r.text[:100] }")

#Test NewsAPI
news_key = os.getenv("NEWS_API_KEY")
r = requests.get(
    "https://newsapi.org/v2/top-headlines",
    params = {"country" : "es", "apiKey" : news_key}
)

print(f"NewsAPI: {r.status_code} - {'Ok' if r.status_code == 200 else 'Error: ' + r.text[:100] }")