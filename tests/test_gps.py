# Script para probar la lógica de la función Haversine, que simula el GPS.

import math
import time

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calcula la distancia Haversine entre dos puntos.
    (Función extraída del código principal para pruebas de unidad).
    """
    R = 6371000  # Radio de la Tierra en metros
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Puntos de prueba para validar la función Haversine.
test_points = [
    {"name": "Punto A", "lat": 9.93310, "lon": -84.03220},
    {"name": "Punto B", "lat": 9.93315, "lon": -84.03225}, # Distancia pequeña
    {"name": "Punto C", "lat": 9.93400, "lon": -84.03300}, # Distancia mayor
]

# Inicia la prueba.
print("Iniciando prueba de la función de distancia Haversine...")

# Prueba 1: Distancia muy corta.
dist_1 = haversine_distance(test_points[0]["lat"], test_points[0]["lon"], 
                             test_points[1]["lat"], test_points[1]["lon"])
print(f"Distancia entre {test_points[0]['name']} y {test_points[1]['name']}: {dist_1:.2f} metros.")
if 1 <= dist_1 <= 10:
    print("Resultado: ¡Correcto! La distancia es razonable.")
else:
    print("Resultado: ¡Fallo! La distancia calculada no es la esperada.")

# Prueba 2: Distancia un poco mayor.
dist_2 = haversine_distance(test_points[0]["lat"], test_points[0]["lon"], 
                             test_points[2]["lat"], test_points[2]["lon"])
print(f"Distancia entre {test_points[0]['name']} y {test_points[2]['name']}: {dist_2:.2f} metros.")
if 50 <= dist_2 <= 100:
    print("Resultado: ¡Correcto! La distancia es razonable.")
else:
    print("Resultado: ¡Fallo! La distancia calculada no es la esperada.")

print("Prueba de distancia Haversine finalizada.")
