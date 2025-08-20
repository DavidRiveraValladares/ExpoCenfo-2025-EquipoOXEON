# EJEMPLO: DEMOSTRACIÓN DE CONEXIÓN Y USO DE LA API DE GEMINI

# Este script se conecta a Wi-Fi y luego envía una pregunta simple a Gemini
# para demostrar que la comunicación con la API funciona.

import wifi
import socketpool
import ssl
import adafruit_requests as requests
from secrets import secrets

# --- CONFIGURACIÓN DE LA API ---
API_KEY = secrets["api_key"]
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

# --- CONEXIÓN AL WI-FI ---
try:
    print("Conectando al WiFi...")
    wifi.radio.connect(secrets["ssid"], secrets["password"])
    print("¡WiFi conectado!")
except ConnectionError:
    print("Error de conexión WiFi. Revisa tu archivo secrets.py")
    exit()

# --- PREPARACIÓN PARA LA LLAMADA A LA API ---
socket = socketpool.SocketPool(wifi.radio)
https = requests.Session(socket, ssl.create_default_context())

def preguntar_gemini(pregunta):
    """Envía una pregunta a la API de Gemini y retorna la respuesta."""
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": pregunta}]}],
        "generationConfig": {"maxOutputTokens": 30}
    }
    try:
        response = https.post(ENDPOINT, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            data = response.json()
            respuesta = data["candidates"][0]["content"]["parts"][0]["text"]
            return respuesta
        else:
            return f"Error en la API: {response.status_code}"
    except Exception as e:
        return f"Excepción al llamar a la API: {e}"

# --- DEMOSTRACIÓN ---
print("\n--- ENVIANDO PREGUNTA A GEMINI ---")
pregunta_ejemplo = "Dime algo interesante sobre Costa Rica en una oración simple."
print(f"Pregunta: '{pregunta_ejemplo}'")

respuesta = preguntar_gemini(pregunta_ejemplo)
print(f"\nRespuesta de Gemini:\n'{respuesta}'")

print("\n--- EJEMPLO COMPLETADO ---")
