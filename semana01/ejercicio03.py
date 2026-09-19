import requests
from dotenv import load_dotenv
import os
import csv
from datetime import datetime

load_dotenv()

try:
    news_key = os.getenv("NEWS_API_KEY")

    #Extracción de las noticias desde la api
    payload = {'country':'us', 'apiKey':news_key}
    r = requests.get(
    "https://newsapi.org/v2/top-headlines",
    timeout = 5,
    params = payload   
    )
    r.raise_for_status()
    newsList = r.json()

    #Aviso de la información extraida
    if newsList['status'] == 'ok':
        if newsList['totalResults'] == 0:
                print('WARNING: No hay ningún resultado')
        else:
            print(f"Se han obtenido {newsList['totalResults']} resultados")
            
            #Gestión y guardado de las noticias en .csv
            path = "semana01/news.csv"
            header = ['FECHA', 'TITULO', 'FUENTE', 'URL']
            errorsAccount = 0
            with open(path, 'w', newline='', encoding='utf-8') as outfile:
                writer = csv.writer(outfile, delimiter=';')
                writer.writerow(header)
                for news in newsList['articles']:
                    try:
                        fecha = datetime.strptime(news['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').strftime('%d/%m/%Y %H:%M')
                        writer.writerow([fecha, news['title'], news['source']['name'], news['url']])
                    except csv.Error:
                        errorsAccount+=1

            print(f'COMPLETADO: Se ha guardado la información en: {path}')
            if errorsAccount > 0:
                print(f'Se han producido errores en {errorsAccount} líneas')
    else:
        print("El estado de la respuesta no es correcto. Revisa la petición.")

except requests.exceptions.ConnectionError:
    print("Error: no hay conexión")
except requests.exceptions.Timeout:
    print("Error: timeout")
except requests.exceptions.HTTPError as e:
    print(f"Error HTTP: {e}")