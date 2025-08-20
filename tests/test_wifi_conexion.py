# Script para probar la conexión WiFi.

import time
import wifi
from secrets import secrets

# Intenta conectar al WiFi.
print("Iniciando prueba de conexión WiFi...")
try:
    print(f"Conectando a {secrets['ssid']}...")
    wifi.radio.connect(secrets["ssid"], secrets["password"])
    print("¡Éxito! Conectado a la red WiFi.")
    print(f"Dirección IP: {wifi.radio.ipv4_address}")
    
    # Muestra un mensaje de éxito por un tiempo para verificar.
    time.sleep(5)
    
except ConnectionError as e:
    print("¡Fallo! No se pudo conectar al WiFi.")
    print(f"Error de conexión: {e}")
except Exception as e:
    print("¡Fallo! Ocurrió un error inesperado.")
    print(f"Error: {e}")
    
finally:
    print("Prueba de conexión WiFi finalizada.")
