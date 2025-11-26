"""
Script de Prueba - Generador de Consultas
EP3_ISY0101 - Implementación de Observabilidad

Este script genera consultas de prueba automáticamente para poblar el dashboard.
"""

import requests
import time
import random

API_URL = "http://localhost:5000"

# Preguntas de ejemplo
PREGUNTAS_EJEMPLO = [
    "¿Qué es una caries dental?",
    "¿Cómo se realiza una limpieza dental?",
    "¿Es seguro el blanqueamiento dental?",
    "¿Cuánto dura un tratamiento de ortodoncia?",
    "¿Qué es un implante dental?",
    "¿Por qué tengo sensibilidad dental?",
    "¿Qué es una endodoncia?",
    "¿Cómo se trata la enfermedad periodontal?",
    "¿Cuándo es necesaria una extracción dental?",
    "¿Qué es una corona dental?",
    "¿Cómo prevenir las caries?",
    "¿Cada cuánto debo ir al dentista?",
    "¿Qué causa el mal aliento?",
    "¿Cómo cuidar mis dientes después de una extracción?",
    "¿Qué son las carillas dentales?"
]


def verificar_api():
    """Verifica que la API esté disponible."""
    try:
        response = requests.get(f"{API_URL}/api/health", timeout=2)
        if response.status_code == 200:
            print("✓ API disponible")
            return True
        else:
            print("✗ API no responde correctamente")
            return False
    except requests.exceptions.RequestException:
        print("✗ No se pudo conectar con la API")
        print("  Asegúrate de ejecutar: python api_flask.py")
        return False


def registrar_consulta(pregunta):
    """Registra una consulta en la API."""
    try:
        response = requests.post(
            f"{API_URL}/api/registrar_consulta",
            json={"pregunta": pregunta},
            timeout=2
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Consulta #{data['execution_id']} registrada: {pregunta[:50]}...")
            return True
        else:
            print(f"✗ Error al registrar consulta: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ Error de conexión: {e}")
        return False


def generar_consultas_prueba(cantidad=10, intervalo=1):
    """
    Genera consultas de prueba.
    
    Args:
        cantidad: Número de consultas a generar
        intervalo: Tiempo de espera entre consultas (segundos)
    """
    print(f"\n{'='*60}")
    print("GENERADOR DE CONSULTAS DE PRUEBA")
    print(f"{'='*60}\n")
    
    if not verificar_api():
        return
    
    print(f"\nGenerando {cantidad} consultas de prueba...")
    print(f"Intervalo entre consultas: {intervalo} segundo(s)\n")
    
    exitosas = 0
    fallidas = 0
    
    for i in range(cantidad):
        pregunta = random.choice(PREGUNTAS_EJEMPLO)
        
        if registrar_consulta(pregunta):
            exitosas += 1
        else:
            fallidas += 1
        
        if i < cantidad - 1:  # No esperar después de la última
            time.sleep(intervalo)
    
    print(f"\n{'='*60}")
    print("RESUMEN")
    print(f"{'='*60}")
    print(f"Total de consultas: {cantidad}")
    print(f"Exitosas: {exitosas}")
    print(f"Fallidas: {fallidas}")
    print(f"\n✓ Abre dashboard.html para ver las métricas actualizadas")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    # Generar 15 consultas con 0.5 segundos de intervalo
    generar_consultas_prueba(cantidad=15, intervalo=0.5)
