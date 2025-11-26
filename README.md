# 🦷 Sistema de Observabilidad para Agente de IA Dental

## 📋 Descripción

Sistema de observabilidad completo para un agente de IA especializado en odontología. El sistema incluye:

- **Agente de Preguntas**: Interfaz interactiva para hacer preguntas sobre odontología
- **API Flask**: Backend que gestiona métricas de observabilidad y seguridad
- **Dashboard Web**: Visualización en tiempo real de métricas y alertas de seguridad

## 🚀 Características

### Métricas de Observabilidad
- ✅ Latencia de respuestas
- ✅ Tasa de éxito/fallo
- ✅ Frecuencia de errores por tipo
- ✅ Historial de ejecuciones

### Métricas de Seguridad
- 🔒 Intentos de acceso no autorizado
- 🔒 Consultas maliciosas bloqueadas
- 🔒 Tokens validados
- 🔒 Sesiones activas
- 🔒 Alertas de seguridad en tiempo real

## 📦 Instalación

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Verificar instalación

```bash
python -c "import flask; import requests; print('✓ Dependencias instaladas correctamente')"
```

## 🎯 Uso

### Paso 1: Iniciar la API Flask

Abre una terminal y ejecuta:

```bash
python api_flask.py
```

La API estará disponible en `http://localhost:5000`

**Endpoints disponibles:**
- `GET /api/metricas` - Métricas agregadas de observabilidad
- `GET /api/ejecuciones` - Lista de ejecuciones recientes
- `GET /api/seguridad` - Métricas de seguridad
- `POST /api/registrar_consulta` - Registrar nueva consulta
- `GET /api/health` - Health check del servicio

### Paso 2: Abrir el Dashboard

Abre el archivo `dashboard.html` en tu navegador web. El dashboard se actualizará automáticamente cada 5 segundos.

### Paso 3: Usar el Agente de Preguntas

En otra terminal, ejecuta:

```bash
python agente_preguntas.py
```

Ahora puedes hacer preguntas sobre temas dentales como:
- Caries y prevención
- Limpieza dental
- Blanqueamiento
- Ortodoncia
- Implantes dentales
- Sensibilidad dental
- Endodoncia
- Enfermedad periodontal
- Extracción dental
- Coronas dentales

**Ejemplo de uso:**
```
💬 Tu pregunta: ¿Qué es la caries dental?
🦷 Respuesta: La caries dental es una enfermedad causada por bacterias...
```

## 🏗️ Arquitectura

```
┌─────────────────┐
│ Agente Preguntas│
│  (Python CLI)   │
└────────┬────────┘
         │
         │ POST /api/registrar_consulta
         ▼
┌─────────────────┐
│   API Flask     │◄────── GET /api/metricas ──────┐
│  (Backend)      │                                 │
└─────────────────┘                                 │
         │                                          │
         │ Métricas en memoria                      │
         │ (sin archivos JSON)                      │
         │                                          │
         └──────────────────────────────────────────┤
                                                    │
                                            ┌───────┴────────┐
                                            │   Dashboard    │
                                            │   (HTML/JS)    │
                                            └────────────────┘
```

## 📊 Dashboard

El dashboard muestra:

1. **Sección de Seguridad** (parte superior)
   - Nivel de seguridad del sistema
   - Métricas de seguridad en tiempo real
   - Alertas activas

2. **Métricas de Observabilidad**
   - Ejecuciones totales
   - Tasa de éxito
   - Latencia promedio
   - Errores detectados

3. **Gráficos Interactivos**
   - Latencia en el tiempo
   - Ratio éxito vs falla
   - Frecuencia de errores por tipo

## 🔧 Configuración

### Cambiar puerto de la API

Edita `api_flask.py` y modifica la última línea:

```python
app.run(debug=True, host='0.0.0.0', port=5000)  # Cambia el puerto aquí
```

### Cambiar URL de la API en el dashboard

Edita `dashboard.html` y modifica:

```javascript
const API_URL = 'http://localhost:5000';  // Cambia la URL aquí
```

### Cambiar URL de la API en el agente

Edita `agente_preguntas.py` y modifica:

```python
agente = AgentePreguntas(api_url="http://localhost:5000")  # Cambia la URL aquí
```

## 📝 Notas Importantes

- ✅ **Sin archivos JSON**: Todas las métricas se almacenan en memoria en la API
- ✅ **Actualización en tiempo real**: El dashboard se actualiza automáticamente cada 5 segundos
- ✅ **Límite de ejecuciones**: La API almacena las últimas 100 ejecuciones en memoria
- ✅ **CORS habilitado**: El dashboard puede consumir la API desde cualquier origen

## 🛠️ Solución de Problemas

### Error: "No se pudo conectar con la API"

**Solución**: Asegúrate de que la API Flask esté corriendo:
```bash
python api_flask.py
```

### Error: "ModuleNotFoundError: No module named 'flask'"

**Solución**: Instala las dependencias:
```bash
pip install -r requirements.txt
```

### El dashboard no muestra datos

**Solución**: 
1. Verifica que la API esté corriendo
2. Ejecuta el agente para generar datos:
   ```bash
   python agente_preguntas.py
   ```
3. Haz algunas preguntas al agente

## 📚 Estructura de Archivos

```
Prueba_3/
├── api_flask.py              # API Flask con endpoints de métricas
├── agente_preguntas.py       # Agente interactivo de preguntas
├── dashboard.html            # Dashboard web de visualización
├── requirements.txt          # Dependencias de Python
└── README.md                 # Este archivo
```

## 🎓 Evaluación EP3_ISY0101

Este proyecto implementa:

1. **Observabilidad**: Métricas de latencia, precisión y errores
2. **Trazabilidad**: Registro de todas las ejecuciones con timestamps
3. **Visualización**: Dashboard interactivo con gráficos en tiempo real
4. **Seguridad**: Monitoreo de eventos de seguridad y alertas
5. **API REST**: Arquitectura moderna con separación de responsabilidades

## 👨‍💻 Autor

Estudiante - EP3_ISY0101
Fecha: 2025

## 📄 Licencia

Este proyecto es parte de una evaluación académica.
