# 🌐 DescubreCR: Guía Interactiva de Puntos de Interés con Geolocalización

## 🧠 Resumen Ejecutivo

**DescubreCR** es un sistema ciberfísico que detecta automáticamente la ubicación geográfica del usuario mediante un microcontrolador con GPS, y despliega información contextual y cultural sobre el sitio en tiempo real. Esta solución interactiva combina hardware embebido con generación dinámica de contenido a través de inteligencia artificial, permitiendo explorar espacios como campus, parques o zonas turísticas de forma educativa y personalizada. El proyecto responde al reto de **ExpoCenfo 2025** de crear *Soluciones para el Mundo Real*.

---

## 1. Información del Proyecto

**Nombre del Proyecto:** DescubreCR – Guía Interactiva de Puntos de Interés  
**Evento:** ExpoCenfo 2025

**Equipo:**
- David Rivera Valladares
- Sebastián Cruz González
- Nathan Esquivel Méndez
- Cristopher Gutiérrez Vega

**Roles:**
- 🛠️ [Integrante 1]: Desarrollador de firmware y lógica del microcontrolador.  
- 🎨 [Integrante 2]: Diseñador UX/UI y encargado del prototipo físico.  
- 📚 [Integrante 3]: Investigador e integrador de la API de lenguaje natural.

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
- Mostrar la información mediante pantalla OLED o salida de audio.

---

## 4. Requisitos Iniciales

- ✅ El dispositivo debe obtener coordenadas mediante el módulo GPS.  
- ✅ El sistema debe detectar cuando está a menos de 500 metros de un POI.  
- ✅ Al llegar a un POI, debe mostrar una descripción automática.  
- ✅ Las descripciones pueden generarse vía **IA (Gemini API)** para personalización.

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
#include <TinyGPSPlus.h>
#include <HardwareSerial.h>

// Configuración del GPS
TinyGPSPlus gps;
HardwareSerial GPS_Serial(1);  // UART1 para GPS

void setup() {
  Serial.begin(115200);       // Monitor Serial
  GPS_Serial.begin(9600, SERIAL_8N1, 16, 17); // RX=16, TX=17 (ajustar según conexión)

  Serial.println("Iniciando módulo GPS...");
}

void loop() {
  while (GPS_Serial.available() > 0) {
    char c = GPS_Serial.read();
    gps.encode(c);

    if (gps.location.isUpdated()) {
      float lat = gps.location.lat();
      float lng = gps.location.lng();

      Serial.print("Latitud: ");
      Serial.println(lat, 6);
      Serial.print("Longitud: ");
      Serial.println(lng, 6);

      // Ejemplo: detección básica de punto de interés (simulado)
      if (isNear(lat, lng, 9.93333, -84.08333, 0.001)) {
        Serial.println(">> Estás cerca de San José Centro");
      }
    }
  }
}

// Función para verificar cercanía a un punto objetivo (lat, lng, radio en grados)
bool isNear(float lat1, float lng1, float lat2, float lng2, float radius) {
  return (abs(lat1 - lat2) < radius) && (abs(lng1 - lng2) < radius);
}
