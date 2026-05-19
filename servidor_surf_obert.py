import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import socket
import time
from datetime import datetime
import math

# Base de dades de ubicacions
spots_db = {
    "Andalusia": [
        {"nom": "El Palmar", "lat": 36.236, "lon": -6.071, "orientacio": 240},
        {"nom": "Tarifa", "lat": 36.013, "lon": -5.606, "orientacio": 220},
        {"nom": "Yerbabuena", "lat": 36.183, "lon": -5.992, "orientacio": 250},
        {"nom": "Cabopino", "lat": 36.488, "lon": -4.744, "orientacio": 180},
        {"nom": "Punta Umbria", "lat": 37.178, "lon": -6.966, "orientacio": 230},
        {"nom": "Los Bateles", "lat": 36.273, "lon": -6.089, "orientacio": 240},
        {"nom": "Canos de Meca", "lat": 36.182, "lon": -6.011, "orientacio": 250},
        {"nom": "Cortadura", "lat": 36.494, "lon": -6.265, "orientacio": 230},
        {"nom": "Mazagon", "lat": 37.135, "lon": -6.822, "orientacio": 220},
        {"nom": "Santa Amalia", "lat": 36.536, "lon": -4.618, "orientacio": 180}
    ],
    "Asturies": [
        {"nom": "Salinas", "lat": 43.578, "lon": -5.955, "orientacio": 340},
        {"nom": "Rodiles", "lat": 43.533, "lon": -5.383, "orientacio": 10},
        {"nom": "Xago", "lat": 43.611, "lon": -5.918, "orientacio": 350},
        {"nom": "San Lorenzo", "lat": 43.543, "lon": -5.654, "orientacio": 20},
        {"nom": "Playa Espana", "lat": 43.545, "lon": -5.597, "orientacio": 0},
        {"nom": "Tapia", "lat": 43.571, "lon": -6.945, "orientacio": 330},
        {"nom": "Penarronda", "lat": 43.554, "lon": -6.992, "orientacio": 320},
        {"nom": "San Antolin", "lat": 43.438, "lon": -4.869, "orientacio": 350},
        {"nom": "Vega", "lat": 43.486, "lon": -5.143, "orientacio": 10},
        {"nom": "Frejulfe", "lat": 43.559, "lon": -6.658, "orientacio": 330}
    ],
    "Canaries": [
        {"nom": "Famara", "lat": 29.116, "lon": -13.556, "orientacio": 300},
        {"nom": "Las Americas", "lat": 28.058, "lon": -16.732, "orientacio": 210},
        {"nom": "El Quemao", "lat": 29.117, "lon": -13.633, "orientacio": 310},
        {"nom": "Los Lobos", "lat": 28.749, "lon": -13.818, "orientacio": 270},
        {"nom": "El Confital", "lat": 28.163, "lon": -15.441, "orientacio": 300},
        {"nom": "La Santa", "lat": 29.109, "lon": -13.651, "orientacio": 310},
        {"nom": "El Socorro", "lat": 28.396, "lon": -16.602, "orientacio": 350},
        {"nom": "Punta Blanca", "lat": 28.212, "lon": -16.836, "orientacio": 260},
        {"nom": "Igueste", "lat": 28.536, "lon": -16.152, "orientacio": 70},
        {"nom": "Bajamar", "lat": 28.556, "lon": -16.345, "orientacio": 30}
    ],
    "Cantabria": [
        {"nom": "Somo", "lat": 43.454, "lon": -3.765, "orientacio": 20},
        {"nom": "Los Locos", "lat": 43.435, "lon": -4.045, "orientacio": 350},
        {"nom": "Laredo", "lat": 43.415, "lon": -3.432, "orientacio": 30},
        {"nom": "Berria", "lat": 43.458, "lon": -3.468, "orientacio": 40},
        {"nom": "Liencres", "lat": 43.468, "lon": -3.938, "orientacio": 340},
        {"nom": "Meron", "lat": 43.391, "lon": -4.385, "orientacio": 350},
        {"nom": "Santa Marina", "lat": 43.453, "lon": -3.738, "orientacio": 20},
        {"nom": "Langre", "lat": 43.477, "lon": -3.702, "orientacio": 10},
        {"nom": "Galizano", "lat": 43.481, "lon": -3.674, "orientacio": 20},
        {"nom": "Suances", "lat": 43.437, "lon": -4.038, "orientacio": 350}
    ],
    "Catalunya": [
        {"nom": "Barceloneta", "lat": 41.378, "lon": 2.192, "orientacio": 120},
        {"nom": "Sitges", "lat": 41.233, "lon": 1.804, "orientacio": 180},
        {"nom": "Masnou", "lat": 41.478, "lon": 2.313, "orientacio": 110},
        {"nom": "Montgat", "lat": 41.464, "lon": 2.279, "orientacio": 120},
        {"nom": "Castelldefels", "lat": 41.264, "lon": 1.993, "orientacio": 170},
        {"nom": "Premia de Mar", "lat": 41.491, "lon": 2.359, "orientacio": 110},
        {"nom": "Bogatell", "lat": 41.393, "lon": 2.207, "orientacio": 120},
        {"nom": "Garraf", "lat": 41.253, "lon": 1.901, "orientacio": 160},
        {"nom": "Riu Besos", "lat": 41.417, "lon": 2.232, "orientacio": 110},
        {"nom": "Blanes", "lat": 41.673, "lon": 2.795, "orientacio": 130}
    ],
    "Galicia": [
        {"nom": "Razo", "lat": 43.292, "lon": -8.705, "orientacio": 300},
        {"nom": "Pantin", "lat": 43.638, "lon": -8.109, "orientacio": 310},
        {"nom": "Doninos", "lat": 43.498, "lon": -8.318, "orientacio": 300},
        {"nom": "A Lanzada", "lat": 42.433, "lon": -8.878, "orientacio": 260},
        {"nom": "Patos", "lat": 42.146, "lon": -8.824, "orientacio": 280},
        {"nom": "Nemina", "lat": 43.013, "lon": -9.231, "orientacio": 290},
        {"nom": "Sabon", "lat": 43.328, "lon": -8.504, "orientacio": 300},
        {"nom": "Bastiagueiro", "lat": 43.344, "lon": -8.349, "orientacio": 310},
        {"nom": "Soesto", "lat": 43.208, "lon": -9.022, "orientacio": 300},
        {"nom": "Rio Sieira", "lat": 42.648, "lon": -9.034, "orientacio": 280}
    ],
    "Pais_Basc": [
        {"nom": "Mundaka", "lat": 43.407, "lon": -2.697, "orientacio": 30},
        {"nom": "Zarautz", "lat": 43.285, "lon": -2.164, "orientacio": 20},
        {"nom": "Sopelana", "lat": 43.388, "lon": -2.996, "orientacio": 350},
        {"nom": "Bakio", "lat": 43.428, "lon": -2.808, "orientacio": 20},
        {"nom": "Zurriola", "lat": 43.326, "lon": -1.975, "orientacio": 40},
        {"nom": "Menakoz", "lat": 43.395, "lon": -2.984, "orientacio": 350},
        {"nom": "Laga", "lat": 43.411, "lon": -2.651, "orientacio": 30},
        {"nom": "Karraspio", "lat": 43.366, "lon": -2.497, "orientacio": 40},
        {"nom": "Orrua", "lat": 43.303, "lon": -2.224, "orientacio": 20},
        {"nom": "Playa Gris", "lat": 43.305, "lon": -2.235, "orientacio": 20}
    ]
}




def factor_swell(orientacio, dir_onada):
    diff = abs(orientacio - dir_onada)
    diff = min(diff, 360 - diff)
    return max(0, math.cos(math.radians(diff)))  # evitem negatius

def factor_vent_orientacio(orientacio, dir_vent):
    offshore = (orientacio + 180) % 360
    diff = abs(offshore - dir_vent)
    diff = min(diff, 360 - diff)
    return math.cos(math.radians(diff))

def factor_vent_velocitat(vent):
    return 1 / (1 + math.log1p(vent))

def calcular_score(onada, dir_onada, periode, vent, dir_vent, orientacio):
    fs = factor_swell(orientacio, dir_onada)
    fv_dir = factor_vent_orientacio(orientacio, dir_vent)
    fv_vel = factor_vent_velocitat(vent)

    return onada * (1 + 0.5 * fs) * (1 + 0.7 * fv_dir) *fv_vel * (periode/10)

def tipus_vent(orientacio, dir_vent):
    offshore = (orientacio + 180) % 360
    
    diff = abs(offshore - dir_vent)
    diff = min(diff, 360 - diff)

    if diff <= 45:
        return "OFFSHORE"
    elif diff >= 135:
        return "ONSHORE"
    else:
        return "CROSSSHORE"

def calcular_top_5_comunitat(comunitat):
    hora_actual = datetime.now().hour
    resultats = []

    llista_spots = spots_db.get(comunitat, spots_db["Cantabria"])

    print(f"\n[{comunitat}] Calculant el Top 5 per a les próximes 24h...")

    for spot in llista_spots:
        ##url = f"https://marine-api.open-meteo.com/v1/marine?latitude={spot['lat']}&longitude={spot['lon']}&hourly=wave_height,wave_period,wave_direction,wind_speed_10m,wind_direction_10m,sea_surface_temperature&forecast_days=2&timezone=Europe/Berlin"
        url_mar = f"https://marine-api.open-meteo.com/v1/marine?latitude={spot['lat']}&longitude={spot['lon']}&hourly=wave_height,wave_period,wave_direction,sea_surface_temperature&forecast_days=2&timezone=Europe/Madrid"

        url_vent = f"https://api.open-meteo.com/v1/forecast?latitude={spot['lat']}&longitude={spot['lon']}&hourly=wind_speed_10m,wind_direction_10m&forecast_days=2&timezone=Europe/Madrid"

        exito = False
        intents = 0

        while not exito and intents < 3:
            try:
                ##resposta = requests.get(url, timeout=5).json()

                resposta_mar = requests.get(url_mar, timeout=5).json()
                resposta_vent = requests.get(url_vent, timeout=5).json()

                millor_score = 0.0
                previsio_spot = []

                for i in range(hora_actual, hora_actual + 12):
                    onada = resposta_mar["hourly"]["wave_height"][i]
                    periode = resposta_mar["hourly"]["wave_period"][i]
                    dir_onada = resposta_mar["hourly"]["wave_direction"][i]
                    vent = resposta_vent["hourly"]["wind_speed_10m"][i]
                    dir_vent = resposta_vent["hourly"]["wind_direction_10m"][i]

                    tipus = tipus_vent(spot["orientacio"], dir_vent)

                    score = calcular_score(onada,dir_onada,periode,vent,dir_vent,spot["orientacio"])

                    if score > millor_score:
                        millor_score = score

                    temps = resposta_mar["hourly"]["time"][i]
                    dia = int(temps[8:10])
                    mes = int(temps[5:7])

                    previsio_spot.append({
                        "data": f"{dia}/{mes}",
                        "hora": temps[11:16],
                        "onada": onada,
                        "periode": periode,
                        "temp": resposta_mar["hourly"]["sea_surface_temperature"][i],
                        "vent": vent,
                        "dir_vent": dir_vent,
                        "dir_onada": dir_onada,
                        "tipus_vent": tipus,
                        "score": round(score, 3)
                    })

                resultats.append({
                    "nom": spot["nom"],
                    "score": millor_score,
                    "previsio": previsio_spot
                })

                exito = True

            except Exception as e:
                intents += 1
                print(f"  -> Error llegint {spot['nom']} (Intent {intents}/3). Reintentant...")
                time.sleep(1)

        time.sleep(0.2)

    # ORDENAR PER SCORE
    resultats.sort(key=lambda x: x["score"], reverse=True)
    top_5 = resultats[:5]

    csv_final = ""
    for index, spot in enumerate(top_5):
        csv_final += f"{spot['nom']}\n"
        for p in spot['previsio']:
            csv_final += f"{p['data']},{p['hora']},{p['onada']},{p['periode']},{p['temp']},{p['vent']},{p['dir_vent']},{p['dir_onada']},{p['tipus_vent']},{p['score']}\n"
        if index < len(top_5) - 1:
            csv_final += "---\n"

    print(f"Calculant el Top 5.")
    return csv_final


class Manejador(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query = parse_qs(parsed_path.query)
        regio = query.get('regio', ['Cantabria'])[0] 
        
        print(f"\n--> Arduino ha solicitado datos de: {regio}")
        csv_data = calcular_top_5_comunitat(regio)
        
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(csv_data.encode('utf-8'))

#Unic canvi del codi tancat al codi obert. eliminem la funcio Obtenir_ip que ja no es necesari 
if __name__ == '__main__':
    # Llegim el port de la variable d'entorn que assigna el servidor (per defecte 8080 si ho corres en local)
    puerto = int(os.environ.get('PORT', 8080))
    
    print("="*50)
    print(f"Servidor iniciat (Port dinàmic: {puerto})")
    print("="*50)
    
    servidor = HTTPServer(('0.0.0.0', puerto), Manejador)
    servidor.serve_forever()
