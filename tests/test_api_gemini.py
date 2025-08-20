# Script para probar la comunicación con la API de Gemini.

import socketpool
import ssl
import wifi
import adafruit_requests as requests
from secrets import secrets

# Configuración de la API.
API_KEY = secrets["api_key"]
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

# Conexión al WiFi (necesaria para la prueba de la API).
try:
    wifi.radio.connect(secrets["ssid"], secrets["password"])
    print(f"Conectado a la red WiFi: {secrets['ssid']}")
except ConnectionError:
    print("No se pudo conectar al WiFi. Asegúrate de que las credenciales son correctas.")
    exit()

# Inicializa la sesión HTTPS.
socket = socketpool.SocketPool(wifi.radio)
https = requests.Session(socket, ssl.create_default_context())

def test_api_call():
    """Realiza una llamada de prueba a la API de Gemini."""
    print("Iniciando prueba de la API de Gemini...")
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": "Hola, Gemini. Dame una respuesta corta."}]}],
        "generationConfig": {"maxOutputTokens": 30}
    }
    
    try:
        response = https.post(ENDPOINT, headers=headers, json=payload, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            respuesta = data["candidates"][0]["content"]["parts"][0]["text"]
            print("¡Éxito! Llamada a la API exitosa.")
            print("Respuesta de Gemini:", respuesta)
            return True
        else:
            print(f"¡Fallo! La API respondió con un error.")
            print(f"Código de estado: {response.status_code}")
            print(f"Cuerpo de la respuesta: {response.text}")
            return False
            
    except Exception as e:
        print("¡Fallo! Ocurrió una excepción durante la llamada a la API.")
        print(f"Error: {e}")
        return False

# Ejecuta la prueba.
if test_api_call():
    print("Prueba de la API de Gemini finalizada con éxito.")
else:
    print("Prueba de la API de Gemini fallida.")
