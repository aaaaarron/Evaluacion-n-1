from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime
import random
import time
from collections import deque
import psutil

app = Flask(__name__)
CORS(app)  # Permitir CORS para que el dashboard pueda consumir la API

# Almacenamiento en memoria de las ejecuciones (últimas 100)
ejecuciones = deque(maxlen=100)
metricas_seguridad = {
    "intentos_acceso_no_autorizado": 0,
    "consultas_maliciosas_bloqueadas": 0,
    "tokens_validados": 0,
    "sesiones_activas": 0,
    "ultimo_escaneo_seguridad": datetime.now().isoformat()
}

# Contador global
contador_ejecuciones = 0


def generar_metrica_ejecucion(pregunta: str, execution_id: int) -> dict:
    """
    Genera una métrica de ejecución simulada.
    
    Args:
        pregunta: Pregunta realizada al agente
        execution_id: ID de la ejecución
        
    Returns:
        Dict con métricas de la ejecución
    """
    # Simular latencia
    latencia_ms = round(random.gauss(300, 150), 2)
    latencia_ms = max(50, min(1000, latencia_ms))
    
    # Simular éxito/fallo (85% éxito)
    es_exitoso = random.random() < 0.85
    
    error_type = None
    if not es_exitoso:
        error_type = random.choice(["timeout", "invalid_input", "llm_error"])
    
    return {
        "timestamp": datetime.now().isoformat(),
        "execution_id": execution_id,
        "pregunta": pregunta[:50],
        "latencia_ms": latencia_ms,
        "estado": "success" if es_exitoso else "failed",
        "error_type": error_type
    }


def actualizar_metricas_seguridad():
    """Actualiza las métricas de seguridad de forma aleatoria."""
    global metricas_seguridad
    
    # Simular eventos de seguridad ocasionales
    if random.random() < 0.1:  # 10% de probabilidad
        metricas_seguridad["intentos_acceso_no_autorizado"] += random.randint(0, 2)
    
    if random.random() < 0.05:  # 5% de probabilidad
        metricas_seguridad["consultas_maliciosas_bloqueadas"] += 1
    
    # Incrementar tokens validados
    metricas_seguridad["tokens_validados"] += random.randint(1, 3)
    
    # Sesiones activas (entre 0 y 5)
    metricas_seguridad["sesiones_activas"] = random.randint(0, 5)
    
    metricas_seguridad["ultimo_escaneo_seguridad"] = datetime.now().isoformat()


@app.route('/api/metricas', methods=['GET'])
def obtener_metricas():
    """
    Endpoint que devuelve las métricas agregadas del agente.
    
    Returns:
        JSON con métricas de observabilidad
    """
    if len(ejecuciones) == 0:
        return jsonify({
            "total_ejecuciones": 0,
            "ejecuciones_exitosas": 0,
            "ejecuciones_fallidas": 0,
            "tasa_exito": 0,
            "latencia_promedio": 0,
            "errores_por_tipo": {},
            "timestamp": datetime.now().isoformat()
        })
    
    # Calcular métricas
    total = len(ejecuciones)
    exitosas = sum(1 for e in ejecuciones if e["estado"] == "success")
    fallidas = total - exitosas
    tasa_exito = round((exitosas / total) * 100, 2) if total > 0 else 0
    
    latencias = [e["latencia_ms"] for e in ejecuciones]
    latencia_promedio = round(sum(latencias) / len(latencias), 2) if latencias else 0
    
    # Contar errores por tipo
    errores_por_tipo = {}
    for e in ejecuciones:
        if e["error_type"]:
            errores_por_tipo[e["error_type"]] = errores_por_tipo.get(e["error_type"], 0) + 1
    
    return jsonify({
        "total_ejecuciones": total,
        "ejecuciones_exitosas": exitosas,
        "ejecuciones_fallidas": fallidas,
        "tasa_exito": tasa_exito,
        "latencia_promedio": latencia_promedio,
        "errores_por_tipo": errores_por_tipo,
        "timestamp": datetime.now().isoformat()
    })


@app.route('/api/ejecuciones', methods=['GET'])
def obtener_ejecuciones():
    """
    Endpoint que devuelve las últimas ejecuciones.
    
    Returns:
        JSON con lista de ejecuciones
    """
    return jsonify({
        "ejecuciones": list(ejecuciones),
        "total": len(ejecuciones),
        "timestamp": datetime.now().isoformat()
    })


@app.route('/api/seguridad', methods=['GET'])
def obtener_metricas_seguridad():
    """
    Endpoint que devuelve métricas de seguridad.
    
    Returns:
        JSON con métricas de seguridad
    """
    actualizar_metricas_seguridad()
    
    return jsonify({
        "metricas": metricas_seguridad,
        "nivel_seguridad": calcular_nivel_seguridad(),
        "alertas_activas": generar_alertas_seguridad(),
        "timestamp": datetime.now().isoformat()
    })


def calcular_nivel_seguridad() -> str:
    """
    Calcula el nivel de seguridad basado en las métricas.
    
    Returns:
        Nivel de seguridad: "alto", "medio", "bajo"
    """
    intentos = metricas_seguridad["intentos_acceso_no_autorizado"]
    bloqueadas = metricas_seguridad["consultas_maliciosas_bloqueadas"]
    
    if intentos > 10 or bloqueadas > 5:
        return "bajo"
    elif intentos > 5 or bloqueadas > 2:
        return "medio"
    else:
        return "alto"


def generar_alertas_seguridad() -> list:
    """
    Genera alertas de seguridad basadas en las métricas.
    
    Returns:
        Lista de alertas activas
    """
    alertas = []
    
    if metricas_seguridad["intentos_acceso_no_autorizado"] > 5:
        alertas.append({
            "tipo": "warning",
            "mensaje": f"Múltiples intentos de acceso no autorizado detectados: {metricas_seguridad['intentos_acceso_no_autorizado']}"
        })
    
    if metricas_seguridad["consultas_maliciosas_bloqueadas"] > 3:
        alertas.append({
            "tipo": "danger",
            "mensaje": f"Consultas maliciosas bloqueadas: {metricas_seguridad['consultas_maliciosas_bloqueadas']}"
        })
    
    if metricas_seguridad["sesiones_activas"] > 3:
        alertas.append({
            "tipo": "info",
            "mensaje": f"Alto número de sesiones activas: {metricas_seguridad['sesiones_activas']}"
        })
    
    return alertas


@app.route('/api/registrar_consulta', methods=['POST'])
def registrar_consulta():
    """
    Endpoint para registrar una nueva consulta del agente.
    
    Returns:
        JSON con confirmación
    """
    from flask import request
    
    data = request.get_json()
    pregunta = data.get('pregunta', 'Pregunta no especificada')
    
    global contador_ejecuciones
    metrica = generar_metrica_ejecucion(pregunta, contador_ejecuciones)
    ejecuciones.append(metrica)
    contador_ejecuciones += 1
    
    return jsonify({
        "success": True,
        "execution_id": metrica["execution_id"],
        "mensaje": "Consulta registrada exitosamente"
    })


@app.route('/api/recursos', methods=['GET'])
def obtener_recursos():
    """
    Endpoint que devuelve métricas de recursos del sistema.
    
    Returns:
        JSON con métricas de CPU, memoria, disco y red
    """
    try:
        # CPU
        cpu_percent = psutil.cpu_percent(interval=0.1)
        cpu_count = psutil.cpu_count()
        
        # Memoria
        memoria = psutil.virtual_memory()
        memoria_total_mb = round(memoria.total / (1024 * 1024), 2)
        memoria_usada_mb = round(memoria.used / (1024 * 1024), 2)
        memoria_disponible_mb = round(memoria.available / (1024 * 1024), 2)
        memoria_percent = memoria.percent
        
        # Disco
        disco = psutil.disk_usage('/')
        disco_total_gb = round(disco.total / (1024 * 1024 * 1024), 2)
        disco_usado_gb = round(disco.used / (1024 * 1024 * 1024), 2)
        disco_libre_gb = round(disco.free / (1024 * 1024 * 1024), 2)
        disco_percent = disco.percent
        
        # Red (bytes enviados y recibidos)
        red = psutil.net_io_counters()
        red_enviados_mb = round(red.bytes_sent / (1024 * 1024), 2)
        red_recibidos_mb = round(red.bytes_recv / (1024 * 1024), 2)
        
        return jsonify({
            "cpu": {
                "porcentaje": cpu_percent,
                "nucleos": cpu_count
            },
            "memoria": {
                "total_mb": memoria_total_mb,
                "usada_mb": memoria_usada_mb,
                "disponible_mb": memoria_disponible_mb,
                "porcentaje": memoria_percent
            },
            "disco": {
                "total_gb": disco_total_gb,
                "usado_gb": disco_usado_gb,
                "libre_gb": disco_libre_gb,
                "porcentaje": disco_percent
            },
            "red": {
                "enviados_mb": red_enviados_mb,
                "recibidos_mb": red_recibidos_mb
            },
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Endpoint de health check.
    
    Returns:
        JSON con estado del servicio
    """
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })


if __name__ == '__main__':
    print("\n" + "="*60)
    print("API FLASK - DASHBOARD DE OBSERVABILIDAD")
    print("EP3_ISY0101 - Implementación de Observabilidad")
    print("="*60)
    print("\nEndpoints disponibles:")
    print("  - GET  /api/metricas           - Métricas agregadas")
    print("  - GET  /api/ejecuciones        - Lista de ejecuciones")
    print("  - GET  /api/seguridad          - Métricas de seguridad")
    print("  - GET  /api/recursos           - Recursos del sistema")
    print("  - POST /api/registrar_consulta - Registrar nueva consulta")
    print("  - GET  /api/health             - Health check")
    print("\nServidor corriendo en: http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
