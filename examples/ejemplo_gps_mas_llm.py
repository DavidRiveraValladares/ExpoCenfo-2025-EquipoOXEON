# EJEMPLO: INTEGRACIÓN DE GPS (SIMULADO) Y LA API DE GEMINI

# Este script combina las lógicas de los ejemplos anteriores para
# demostrar cómo el movimiento activa una consulta a Gemini.

import time
import wifi
import socketpool
import ssl
import adafruit_requests as requests
import math
from secrets import secrets

# --- CONFIGURACIÓN DE CONSTANTES Y API ---
API_KEY = secrets["api_key"]
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
UMBRAL_MOVIMIENTO_METROS = 2.0

# --- CONEXIÓN A INTERNET ---
try:
    print("Conectando al WiFi...")
    wifi.radio.connect(secrets["ssid"], secrets["password"])
    print("WiFi conectado.")
except ConnectionError:
    print("Error de conexión WiFi.")
    exit()
socket = socketpool.SocketPool(wifi.radio)
https = requests.Session(socket, ssl.create_default_context())

# --- FUNCIONES ---
def haversine_distance(lat1, lon1, lat2, lon2):
    """Calcula la distancia Haversine entre dos puntos en metros."""
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def preguntar_gemini(pregunta):
    """Envía una pregunta a Gemini y retorna la respuesta."""
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": pregunta}]}],
        "generationConfig": {"maxOutputTokens": 30}
    }
    try:
        response = https.post(ENDPOINT, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"Error en la API: {response.status_code}"
    except Exception as e:
        return f"Excepción al llamar a la API: {e}"

# --- SIMULACIÓN DE RECORRIDO ---
lugares_cenfotec = {
    "Entrada Principal": {"lat": 9.93310, "lon": -84.03220},
    "Maker Space": {"lat": 9.93320, "lon": -84.03210},
}
recorrido_simulado = [lugares_cenfotec["Entrada Principal"], lugares_cenfotec["Sala de Computo"]]
last_location = None

# --- BUCLE PRINCIPAL (DEMO) ---
print("--- INICIANDO DEMO: GPS + IA ---")
print("Simulando movimiento...")
for lugar_actual in recorrido_simulado:
    if last_location is None:
        # Primer punto: siempre se activa la consulta
        distancia = UMBRAL_MOVIMIENTO_METROS + 1
    else:
        distancia = haversine_distance(last_location["lat"], last_location["lon"],
                                       lugar_actual["lat"], lugar_actual["lon"])

    if distancia >= UMBRAL_MOVIMIENTO_METROS:
        print(f"\n¡Movimiento detectado! Distancia: {distancia:.2f} m.")
        
        # El sistema ha "detectado" que llegamos a un nuevo lugar.
        nombre_lugar = [k for k, v in lugares_cenfotec.items() if v == lugar_actual][0]
        
        # Prepara la pregunta para la IA
        pregunta = f"Estoy en la {nombre_lugar} de Cenfotec. Dime algo interesante sobre este lugar."
        print(f"Consultando a Gemini sobre '{nombre_lugar}'...")
        
        respuesta = preguntar_gemini(pregunta)
        print("Respuesta de Gemini:", respuesta)

        # Actualiza la última ubicación
        last_location = lugar_actual
        print("\nEsperando 10 segundos antes de pasar al siguiente punto...")
        time.sleep(10)
    else:
        print(f"Sin suficiente movimiento ({distancia:.2f} m). Esperando...")
        
print("\n--- DEMOSTRACIÓN COMPLETADA ---")
