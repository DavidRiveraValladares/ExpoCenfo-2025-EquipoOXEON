# --- MÓDULO 1: IMPORTACIONES Y CONFIGURACIÓN ---
# Importaciones necesarias para la funcionalidad del proyecto.
import time
import board
import digitalio
import busio
import wifi
import socketpool
import ssl
import adafruit_requests as requests
import math

# El archivo 'secrets.py' debe contener 'ssid', 'password' y 'api_key'.
try:
    from secrets import secrets
except ImportError:
    print("El archivo secrets.py no se ha encontrado. Por favor, crea uno con tus credenciales.")
    exit()

# La librería para el LCD.
from adafruit_character_lcd.character_lcd import Character_LCD_Mono

# --- MÓDULO 2: HARDWARE Y PERIFÉRICOS ---
# Configuración de los pines de la pantalla LCD 16x2.
LCD_PINS = {
    "rs": board.IO21,
    "en": board.IO22,
    "d4": board.IO4,
    "d5": board.IO5,
    "d6": board.IO25,
    "d7": board.IO27,
}
LCD_COLUMNS = 16
LCD_ROWS = 2

# Inicialización del hardware.
try:
    lcd = Character_LCD_Mono(
        digitalio.DigitalInOut(LCD_PINS["rs"]),
        digitalio.DigitalInOut(LCD_PINS["en"]),
        digitalio.DigitalInOut(LCD_PINS["d4"]),
        digitalio.DigitalInOut(LCD_PINS["d5"]),
        digitalio.DigitalInOut(LCD_PINS["d6"]),
        digitalio.DigitalInOut(LCD_PINS["d7"]),
        LCD_COLUMNS,
        LCD_ROWS
    )
    lcd.clear()
except Exception as e:
    print(f"Error al inicializar LCD: {e}")
    # En un escenario real, se podría intentar un reinicio o una recuperación.

# --- MÓDULO 3: CONECTIVIDAD Y API ---
# Constantes para la API de Gemini.
API_KEY = secrets["api_key"]
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
API_RETRY_DELAY = 10  # Retraso en segundos antes de reintentar la llamada a la API.
API_MAX_RETRY = 3     # Número máximo de intentos.

print("Conectando al WiFi...")
lcd.message = "Conectando WiFi"
try:
    wifi.radio.connect(secrets["ssid"], secrets["password"])
    print("Conectado a", secrets["ssid"])
    lcd.clear()
    lcd.message = "WiFi Conectado\n" + secrets["ssid"]
    time.sleep(2)
except ConnectionError:
    print("Error de conexión WiFi. Revisa tus credenciales.")
    lcd.clear()
    lcd.message = "WiFi Error"
    exit()

socket = socketpool.SocketPool(wifi.radio)
https = requests.Session(socket, ssl.create_default_context())

def preguntar_gemini(pregunta):
    """
    Envía una pregunta a la API de Gemini y retorna la respuesta.
    Implementa reintentos en caso de fallo para mejorar la robustez.

    Args:
        pregunta (str): El texto a enviar a Gemini.

    Returns:
        str: La respuesta de Gemini o un mensaje de error.
    """
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": pregunta}]}],
        "generationConfig": {"maxOutputTokens": 30}
    }

    for _ in range(API_MAX_RETRY):
        try:
            response = https.post(ENDPOINT, headers=headers, json=payload, timeout=15)
            if response.status_code == 200:
                data = response.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                print(f"Error de API: {response.status_code}. Reintentando...")
                time.sleep(API_RETRY_DELAY)
        except Exception as e:
            print(f"Excepción en la llamada a la API: {e}. Reintentando...")
            time.sleep(API_RETRY_DELAY)

    return "Error de Gemini. Intenta mas tarde."

# --- MÓDULO 4: LÓGICA DE NEGOCIO Y AYUDAS ---
# Constante para el umbral de movimiento.
UMBRAL_MOVIMIENTO_METROS = 2.0

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calcula la distancia Haversine entre dos puntos en la Tierra.

    Args:
        lat1 (float): Latitud del primer punto en grados.
        lon1 (float): Longitud del primer punto en grados.
        lat2 (float): Latitud del segundo punto en grados.
        lon2 (float): Longitud del segundo punto en grados.

    Returns:
        float: Distancia en metros.
    """
    R = 6371000  # Radio de la Tierra en metros
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def mostrar_en_lcd(texto):
    """
    Muestra un texto largo en la LCD de 16x2, con un efecto de 'scroll'
    pausado para permitir la lectura.
    """
    if len(texto) <= 32:
        lcd.clear()
        lcd.message = texto
        time.sleep(5)
    else:
        for i in range(0, len(texto), 32):
            lcd.clear()
            line1 = texto[i:i+16]
            line2 = texto[i+16:i+32]
            lcd.message = f"{line1}\n{line2}"
            time.sleep(5)
    lcd.clear()

# --- MÓDULO 5: DATOS Y VARIABLES DE ESTADO ---
# Datos de simulación para el recorrido dentro de la universidad.
lugares_cenfotec = {
    "Universidad Cenfotec": {"lat": 9.93310, "lon": -84.03220},
    "Auditorio": {"lat": 9.93282, "lon": -84.03200},
    "Maker Space": {"lat": 9.93305, "lon": -84.03215},
}
recorrido_simulado = [
    {"nombre": "Universidad Cenfotec", "coords": lugares_cenfotec["Universidad Cenfotec"]},
    {"nombre": "Auditorio", "coords": lugares_cenfotec["Auditorio"]},
    {"nombre": "Maker Space", "coords": lugares_cenfotec["Maker Space"]},
]

# Variables para mantener el estado del recorrido simulado.
last_location = None
current_index = 0

# --- MÓDULO 6: BUCLE PRINCIPAL (MAIN LOOP) ---
print("Iniciando sistema ciberfísico...")
while True:
    # Reinicia la simulación si el recorrido ha terminado.
    if current_index >= len(recorrido_simulado):
        print("\nRecorrido terminado. Reiniciando simulación...")
        current_index = 0
        last_location = None
        time.sleep(5)
        continue

    # Obtiene la ubicación actual de la simulación.
    current_location = recorrido_simulado[current_index]

    if last_location is None:
        # En el primer inicio, se fuerza una consulta inicial.
        distancia_movida = UMBRAL_MOVIMIENTO_METROS + 1
    else:
        # Calcula la distancia movida desde la última ubicación.
        distancia_movida = haversine_distance(
            last_location['coords']['lat'], last_location['coords']['lon'],
            current_location['coords']['lat'], current_location['coords']['lon']
        )

    # Evalúa si se ha movido lo suficiente para una nueva consulta.
    if distancia_movida >= UMBRAL_MOVIMIENTO_METROS:
        print(f"\nMovimiento detectado ({distancia_movida:.2f} m).")

        # Prepara y realiza la consulta a la IA.
        pregunta = f"Estoy en {current_location['nombre']}. Dime algo interesante de este lugar en una oración simple."
        print(f"Consultando a Gemini sobre {current_location['nombre']}...")
        lcd.clear()
        lcd.message = "Consultando...\n" + current_location['nombre']

        respuesta = preguntar_gemini(pregunta)
        print("Respuesta de Gemini:", respuesta)

        # Muestra la respuesta en la pantalla LCD.
        mostrar_en_lcd(respuesta)

        # Actualiza el estado y avanza al siguiente punto.
        last_location = current_location
        current_index += 1

        print("Esperando 10 segundos para la siguiente consulta...")
        time.sleep(10) # Pausa para evitar exceder las cuotas de la API.

    else:
        # Si no hay suficiente movimiento, se espera.
        print(f"Esperando movimiento... Distancia: {distancia_movida:.2f} m", end="\r")
        time.sleep(1)
