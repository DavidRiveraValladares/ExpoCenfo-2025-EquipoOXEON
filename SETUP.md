# 🔧 Guía de Instalación

## Requisitos
- IdeaBoard ESP32-WROOM
- Módulo GPS NEO-6M
- Conexión WiFi
- Cuenta en Google Cloud con API Key de Gemini

## Librerías necesarias (CircuitPython)
- adafruit_requests
- adafruit_gps
- digitalio

## Pasos
1. Clona el repositorio.
2. Copia el contenido de `/software/` al ESP32.
3. Asegúrate de tener `secrets.py` con tus credenciales WiFi y API.
4. Ejecuta `code.py` desde el microcontrolador.
