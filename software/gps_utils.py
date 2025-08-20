# gps_utils.py
# Módulo para la lógica de geolocalización.
# Diseñado para interactuar con un sensor GPS real (ej. Neo-6M).

import time
import math
import busio
import board
# Importa la biblioteca Adafruit GPS para manejar el sensor.
# Si no la tienes instalada, debes agregarla a tu carpeta 'lib'.
try:
    import adafruit_gps
except ImportError:
    print("La librería 'adafruit_gps' no se encontró. Instálala para usar un GPS real.")
    adafruit_gps = None

# --- CONFIGURACIÓN DE HARDWARE GPS (COMENTADA) ---
# Esta sección muestra cómo inicializarías el GPS en un proyecto real.
# Debes conectar el GPS a los pines UART (RX y TX) del ESP32.

# try:
#     uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=3000)
#     gps_sensor = adafruit_gps.GPS(uart, debug=False)
#     # Envía comandos al GPS para configurar las sentencias NMEA y la tasa de actualización.
#     gps_sensor.send_command(b"PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
#     gps_sensor.send_command(b"PMTK220,1000") # Actualización cada 1 segundo
# except Exception as e:
#     print(f"Error al inicializar el sensor GPS: {e}")
#     gps_sensor = None


def get_current_location():
    """
    Lee los datos del sensor GPS y retorna la ubicación actual.
    
    Si el sensor no tiene una conexión satelital (fix), retorna None.
    
    Returns:
        dict: Un diccionario con las coordenadas 'lat' y 'lon', o None si no hay datos.
    """
    # En un proyecto real, se usaría esta lógica:
    # if gps_sensor is None:
    #     return None
    # gps_sensor.update()
    # if not gps_sensor.has_fix:
    #     return None
    # return {"lat": gps_sensor.latitude, "lon": gps_sensor.longitude}
    
    # Para la simulación, retornamos None. El código principal manejará la simulación.
    return None


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
