# llm_utils.py
# Módulo para la interacción con la API de Gemini.

import time
import socketpool
import ssl
import adafruit_requests as requests

# Constantes para la API (pueden ser movidas a un archivo de configuración si es necesario)
API_RETRY_DELAY = 10
API_MAX_RETRY = 3

def preguntar_gemini(https_session, endpoint, api_key, pregunta):
    """
    Envía una pregunta a la API de Gemini y retorna la respuesta.
    
    Args:
        https_session (requests.Session): Sesión de requests.
        endpoint (str): URL de la API.
        api_key (str): Clave de la API.
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
            response = https_session.post(endpoint, headers=headers, json=payload, timeout=15)
            if response.status_code == 200:
                data = response.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                print(f"Error de API: {response.status_code}. Reintentando...")
                time.sleep(API_RETRY_DELAY)
        except Exception as e:
            print(f"Excepción en la API: {e}. Reintentando...")
            time.sleep(API_RETRY_DELAY)
            
    return "Error de Gemini. Intenta mas tarde."
