import requests
from dotenv import load_dotenv
import os

load_dotenv()

try:
    ow_key = os.getenv("OPENWEATHER_API_KEY")

    # Primero obtenemos coordenadas de la ciudad porque el endpoint
    # de weather requiere lat/lon, no nombre de ciudad directamente
    payload = {'q':'Alicante', 'appid':ow_key}
    r = requests.get(
        "http://api.openweathermap.org/geo/1.0/direct",
        timeout = 5,
        params = payload   
    )
    r.raise_for_status()
    location = r.json()

    # Después obtenemos el tiempo mediante estas coordenadas obtenidas
    payload = {'lat':location[0]['lat'],'lon':location[0]['lon'],'units':'metric', 'appid':ow_key}
    r = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        timeout = 5,
        params = payload   
    )
    r.raise_for_status()
    weather = r.json()

    print(f"City: {location[0]['name']}, Temp: {weather['main']['temp']} - {weather['weather'][0]['main']}")

    #Añadimos una alerta en caso de lluvia
    if weather['weather'][0]['main']  == 'Rain':
        print("⚠️ Alerta: mañana se esperan lluvias")

#Gestionamos los posibles errores 
except requests.exceptions.ConnectionError:
    print("Error: no hay conexión")
except requests.exceptions.Timeout:
    print("Error: timeout")
except requests.exceptions.HTTPError as e:
    print(f"Error HTTP: {e}")
