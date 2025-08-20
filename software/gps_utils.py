# gps_utils.py
# Módulo para la lógica de geolocalización y cálculo de distancia.

import math

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
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c
