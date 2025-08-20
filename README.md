# 🌐 DescubreCR: Guía Interactiva de Puntos de Interés con Geolocalización

## 🧠 Resumen Ejecutivo

**DescubreCR** es un sistema ciberfísico que detecta automáticamente la ubicación geográfica del usuario mediante un microcontrolador con GPS, y despliega información contextual y cultural sobre el sitio en tiempo real. Esta solución interactiva combina hardware embebido con generación dinámica de contenido a través de inteligencia artificial, permitiendo explorar espacios como campus, parques o zonas turísticas de forma educativa y personalizada. El proyecto responde al reto de **ExpoCenfo 2025** de crear *Soluciones para el Mundo Real*.

> 📸 *[Aquí se incluirá una imagen del prototipo físico o del diagrama de bloques próximamente]*

---

## 1. Información del Proyecto

**Nombre del Proyecto:** DescubreCR – Guía Interactiva de Puntos de Interés  
**Evento:** ExpoCenfo 2025

**Equipo:**
- David Rivera Valladares
- Sebastián Cruz González
- Nathan Esquivel Méndez
- Cristopher Gutiérrez Vega

---

## 👥 Roles del equipo

- 🛠️ **Desarrollador principal de firmware y lógica embebida**  
  **Nombre:** *David R.*  
  Se encarga del desarrollo en CircuitPython, la lógica del GPS, conexión Wi-Fi, integración con APIs y depuración general del código en el ESP32.

- 🎨 **Diseñador UX/UI y modelador del prototipo físico**  
  **Nombre:** *Nathan E.*  
  Responsable del diseño estético del prototipo, bocetos de interfaz, modelado en 3D para impresión y presentación física del sistema.

- 📚 **Investigador técnico y apoyo en integración LLM**  
  **Nombre:** *Sebastián C.*  
  Encargado de investigar documentación oficial de componentes (GPS, Wi-Fi, ESP32), pruebas de compatibilidad, y organización del flujo de consulta al modelo de lenguaje.

- 🧠 **Documentador, apoyo en pruebas y presentaciones**  
  **Nombre:** *Cristopher G.*  
  Lidera la preparación para exposiciones, recopila resultados de pruebas, mantiene la bitácora técnica y asegura la correcta comprensión del funcionamiento por parte del equipo.

> ⚠️ **Nota:** Aunque cada miembro asumió un rol principal, trabajamos en equipo, compartiendo tareas y aprendiendo de forma colaborativa durante todo el proceso.

---

## 2. Descripción y Justificación

### 🧩 Problema que se aborda
Muchas personas carecen de herramientas que ofrezcan información relevante y en tiempo real sobre su entorno físico. Esto afecta la orientación, el aprendizaje contextual y la experiencia del usuario en lugares nuevos o con valor histórico/cultural.

### 🌎 Importancia y contexto
**DescubreCR** propone una guía inteligente basada en geolocalización que enriquece la experiencia de exploración al mostrar contenido informativo automáticamente al llegar a un lugar. Aporta accesibilidad, educación y turismo cultural desde una plataforma embebida.

### 👥 Usuarios beneficiarios
- Estudiantes de nuevo ingreso en campus educativos.  
- Visitantes de zonas turísticas o parques.  
- Organizadores de eventos en espacios físicos amplios.  

---

## 3. Objetivos del Proyecto

### 🎯 Objetivo General
Desarrollar un dispositivo ciberfísico autónomo que detecte la ubicación del usuario y le provea información relevante sobre puntos de interés cercanos.

### 🎯 Objetivos Específicos
- Integrar el microcontrolador **ESP32** con un **módulo GPS**.
- Crear y gestionar una base de datos local de puntos de interés (POIs).
- Detectar cercanía (dentro de 500m) a un POI y mostrar su descripción.
- Integrar una API de LLM (Gemini) para generar descripciones adaptadas al usuario.
- Mostrar la información mediante pantalla OLED y/o salida de audio.

---

## 4. Requisitos Iniciales

- ✅ El dispositivo debe obtener coordenadas mediante el módulo GPS.  
- ✅ El sistema debe detectar cuando está a menos de 500 metros de un POI.  
- ✅ Al llegar a un POI, debe mostrar una descripción automática.  
- ✅ Las descripciones pueden generarse vía **IA (Gemini API)** para personalización.  
- ✅ La base de datos de POIs puede estar embebida en variables, archivo local o futura integración a microSD.

---

## 5. Diseño Preliminar del Sistema

### 🧱 Arquitectura Inicial

> **Componentes previstos:**
- **Microcontrolador:** ESP32-WROOM-32E (IdeaBoard)  
- **Módulo GPS:** NEO-6M  
- **Visualización/Audio:** Pantalla OLED y/o módulo de audio  
- **IA:** Gemini API para generación dinámica de texto  
- **Librerías:** CircuitPython, `adafruit_gps`, `digitalio`, `time`

> **Diagrama de conexión (próximamente):**  
*Se incluirá diagrama de bloques del sistema con flujo de información entre módulos.*

> **Boceto físico (próximamente):**  
*Prototipo 3D en desarrollo. Imagen del dispositivo simulado en pruebas iniciales.*

---

## 6. Plan de Trabajo

| Hito | Descripción | Fecha Estimada |
|------|-------------|----------------|
| Hito 1 | Configuración del módulo GPS con ESP32 | 03 de agosto |
| Hito 2 | Implementación de lógica de detección de POIs | 07 de agosto |
| Hito 3 | Integración de Gemini API para generar descripciones | 10 de agosto |
| Hito 4 | Diseño físico del prototipo y carcasa | 13 de agosto |
| Hito 5 | Ensamblaje completo y pruebas de integración | 16 de agosto |
| Hito 6 | Validación en campo y pruebas finales | 18 de agosto |

---

## 7. Riesgos Identificados y Mitigaciones

| Riesgo | Descripción | Mitigación |
|--------|-------------|------------|
| 📡 Señal GPS débil en interiores | El módulo GPS podría no captar señal en espacios cerrados | Uso de pruebas exteriores y lógica de "última ubicación conocida" |
| ⚠️ Incompatibilidad de librerías | Problemas con `adafruit_gps` en CircuitPython | Documentar errores, buscar alternativas y usar UART directo si es necesario |
| 🔋 Consumo energético alto | Riesgo de que la batería no soporte GPS + pantalla + audio | Optimización de código, uso de batería externa o powerbank |

---

## 8. Prototipo Conceptual – Código de Prueba Simulado

```python
# code.py
# Prototipo de conexión WiFi + consulta a LLM con contexto de ubicación (GPS simulado)
# Proyecto: Sistema ciberfísico basado en ESP32 + IA Generativa
# Autor: [Tu nombre o equipo]
# Fecha: 2025

import time
import wifi
import socketpool
import ssl
import microcontroller
import adafruit_requests
from secrets import secrets

# ------------------------- CONFIGURACIÓN DE GPS -------------------------

# Coordenadas GPS (simuladas) — San José, Costa Rica
GPS_LAT = 9.9333
GPS_LON = -84.0833

# ------------------------- FUNCIÓN: Conectar WiFi -------------------------

def conectar_wifi():
    """Intenta conectar a una red WiFi con credenciales del archivo secrets.py"""
    try:
        print("📡 Conectando a red WiFi...")
        wifi.radio.connect(secrets["ssid"], secrets["password"])
        print("✅ Conectado a", secrets["ssid"])
        print("🌐 Dirección IP:", wifi.radio.ipv4_address)
    except Exception as e:
        print("❌ Error de conexión WiFi:", e)
        time.sleep(3)
        microcontroller.reset()  # Reinicia el microcontrolador si falla la conexión

# ------------------------- FUNCIÓN: Construir prompt -------------------------

def generar_prompt(lat, lon):
    """Crea un prompt personalizado con base en coordenadas GPS"""
    return (
        f"Estoy en las coordenadas {lat}, {lon}. "
        "Dame una breve descripción de este lugar en Costa Rica, usando lenguaje claro."
    )

# ------------------------- FUNCIÓN: Consultar Gemini -------------------------

def consultar_gemini(prompt, api_key):
    """Envía un prompt al modelo Gemini y devuelve la respuesta"""
    API_URL = (
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        f"?key={api_key}"
    )

    headers = {"Content-Type": "application/json"}
    body = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        print("🧠 Consultando modelo generativo...")
        pool = socketpool.SocketPool(wifi.radio)
        session = adafruit_requests.Session(pool, ssl.create_default_context())
        response = session.post(API_URL, headers=headers, json=body)

        if response.status_code == 200:
            result = response.json()
            texto = result["candidates"][0]["content"]["parts"][0]["text"]
            return texto.strip()
        else:
            print(f"⚠️ Error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print("❌ Error en consulta Gemini:", e)
        return None

# ------------------------- MAIN -------------------------

def main():
    conectar_wifi()

    prompt = generar_prompt(GPS_LAT, GPS_LON)
    respuesta = consultar_gemini(prompt, secrets["api_key"])

    if respuesta:
        print("\n📍 Descripción del lugar (generada por IA):")
        print("-" * 50)
        print(respuesta)
        print("-" * 50)
    else:
        print("No se obtuvo respuesta del modelo.")

# Ejecutar programa principal
main()
