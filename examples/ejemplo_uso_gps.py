# EJEMPLO: DEMOSTRACIÓN DE LA LÓGICA DE DETECCIÓN DE MOVIMIENTO (GPS SIMULADO)

# Este script muestra cómo se usa la función Haversine para calcular la distancia
# entre dos puntos y detectar si ha habido suficiente "movimiento".

import math
import time

# --- FUNCIÓN DE DISTANCIA (HA DE SER LA MISMA QUE EN TU CÓDIGO PRINCIPAL) ---
def haversine_distance(lat1, lon1, lat2, lon2):
    """Calcula la distancia Haversine entre dos puntos en metros."""
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# --- VARIABLES DE EJEMPLO ---
UMBRAL_MOVIMIENTO = 2.0  # Umbral de distancia en metros para considerar "movimiento".
ubicacion_inicial = {"lat": 9.93310, "lon": -84.03220}  # Punto A
ubicacion_nueva = {"lat": 9.93315, "lon": -84.03225}    # Punto B, muy cerca
ubicacion_final = {"lat": 9.93350, "lon": -84.03250}    # Punto C, más lejos

# --- DEMOSTRACIÓN ---
print("--- DEMOSTRACIÓN 1: POCO MOVIMIENTO ---")
distancia_corta = haversine_distance(ubicacion_inicial["lat"], ubicacion_inicial["lon"],
                                      ubicacion_nueva["lat"], ubicacion_nueva["lon"])
print(f"Distancia entre A y B: {distancia_corta:.2f} metros.")
if distancia_corta >= UMBRAL_MOVIMIENTO:
    print("Resultado: ¡Movimiento detectado!")
else:
    print("Resultado: No hay suficiente movimiento para activar la acción.")

print("\n--- DEMOSTRACIÓN 2: MOVIMIENTO SIGNIFICATIVO ---")
distancia_larga = haversine_distance(ubicacion_inicial["lat"], ubicacion_inicial["lon"],
                                     ubicacion_final["lat"], ubicacion_final["lon"])
print(f"Distancia entre A y C: {distancia_larga:.2f} metros.")
if distancia_larga >= UMBRAL_MOVIMIENTO:
    print("Resultado: ¡Movimiento detectado!")
else:
    print("Resultado: No hay suficiente movimiento para activar la acción.")

print("\n--- EJEMPLO COMPLETADO ---")
