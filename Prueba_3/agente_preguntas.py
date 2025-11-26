"""
Agente de Preguntas Simplificado
EP3_ISY0101 - Implementación de Observabilidad
Autor: Estudiante
Fecha: 2025

Este script implementa un agente simple donde puedes hacer preguntas.
Las métricas se envían a la API Flask en lugar de guardarse en JSON.
"""

import requests
import time
from datetime import datetime


class AgentePreguntas:
    """
    Agente simple para responder preguntas con integración a API Flask.
    """
    
    def __init__(self, api_url: str = "http://localhost:5000"):
        """
        Inicializa el agente.
        
        Args:
            api_url: URL base de la API Flask
        """
        self.api_url = api_url
        self.verificar_conexion_api()
    
    def verificar_conexion_api(self):
        """Verifica que la API esté disponible."""
        try:
            response = requests.get(f"{self.api_url}/api/health", timeout=2)
            if response.status_code == 200:
                print("✓ Conexión con API establecida")
            else:
                print("⚠ API no responde correctamente")
        except requests.exceptions.RequestException:
            print("⚠ No se pudo conectar con la API. Asegúrate de que esté corriendo.")
            print("   Ejecuta: python api_flask.py")
    
    def procesar_pregunta(self, pregunta: str) -> str:
        """
        Procesa una pregunta y devuelve una respuesta.
        
        Args:
            pregunta: Pregunta del usuario
            
        Returns:
            Respuesta del agente
        """
        print(f"\n🤔 Procesando: {pregunta}")
        
        # Simular procesamiento
        time.sleep(0.5)
        
        # Base de conocimiento simple sobre odontología
        respuestas = {
            "caries": "La caries dental es una enfermedad causada por bacterias que producen ácidos que dañan el esmalte dental. Se previene con buena higiene oral, uso de flúor y visitas regulares al dentista.",
            "limpieza": "Una limpieza dental profesional incluye: eliminación de placa y sarro, pulido dental, y aplicación de flúor. Se recomienda cada 6 meses.",
            "blanqueamiento": "El blanqueamiento dental es seguro cuando se realiza bajo supervisión profesional. Puede causar sensibilidad temporal pero es efectiva para aclarar los dientes.",
            "ortodoncia": "La ortodoncia corrige la posición de los dientes y mandíbula usando brackets, alineadores transparentes u otros dispositivos. El tratamiento dura entre 12-36 meses típicamente.",
            "implante": "Un implante dental es un tornillo de titanio que se coloca en el hueso maxilar para reemplazar la raíz de un diente perdido. Sobre él se coloca una corona artificial.",
            "sensibilidad": "La sensibilidad dental puede deberse a: esmalte desgastado, encías retraídas, caries o grietas. Se trata con pastas especiales, flúor o selladores según la causa.",
            "endodoncia": "La endodoncia o tratamiento de conducto elimina la pulpa infectada del diente, limpia los conductos y los sella. Salva dientes que de otro modo deberían extraerse.",
            "periodoncia": "La enfermedad periodontal afecta las encías y el hueso que sostiene los dientes. Se trata con limpieza profunda, antibióticos y en casos severos, cirugía.",
            "extraccion": "La extracción dental se realiza cuando un diente está muy dañado, infectado o causa problemas de espacio. El proceso es rápido con anestesia local.",
            "corona": "Una corona dental es una funda que cubre completamente un diente dañado. Se usa para proteger, fortalecer y mejorar la apariencia del diente."
        }
        
        # Buscar respuesta relevante
        pregunta_lower = pregunta.lower()
        respuesta = "Lo siento, no tengo información específica sobre esa pregunta. Por favor, consulta con un dentista profesional para obtener asesoramiento personalizado."
        
        for palabra_clave, resp in respuestas.items():
            if palabra_clave in pregunta_lower:
                respuesta = resp
                break
        
        # Registrar en la API
        self.registrar_consulta(pregunta)
        
        return respuesta
    
    def registrar_consulta(self, pregunta: str):
        """
        Registra la consulta en la API Flask.
        
        Args:
            pregunta: Pregunta realizada
        """
        try:
            response = requests.post(
                f"{self.api_url}/api/registrar_consulta",
                json={"pregunta": pregunta},
                timeout=2
            )
            if response.status_code == 200:
                print("✓ Consulta registrada en el sistema de observabilidad")
        except requests.exceptions.RequestException as e:
            print(f"⚠ No se pudo registrar la consulta: {e}")
    
    def iniciar_sesion_interactiva(self):
        """Inicia una sesión interactiva de preguntas y respuestas."""
        print("\n" + "="*60)
        print("AGENTE DE PREGUNTAS - ODONTOLOGÍA")
        print("EP3_ISY0101 - Implementación de Observabilidad")
        print("="*60)
        print("\nPuedes hacer preguntas sobre:")
        print("  • Caries y prevención")
        print("  • Limpieza dental")
        print("  • Blanqueamiento")
        print("  • Ortodoncia")
        print("  • Implantes dentales")
        print("  • Sensibilidad dental")
        print("  • Endodoncia (tratamiento de conducto)")
        print("  • Enfermedad periodontal")
        print("  • Extracción dental")
        print("  • Coronas dentales")
        print("\nEscribe 'salir' para terminar la sesión.")
        print("="*60 + "\n")
        
        while True:
            try:
                pregunta = input("💬 Tu pregunta: ").strip()
                
                if not pregunta:
                    continue
                
                if pregunta.lower() in ['salir', 'exit', 'quit']:
                    print("\n👋 ¡Hasta luego! Cuida tu salud dental.")
                    break
                
                respuesta = self.procesar_pregunta(pregunta)
                print(f"\n🦷 Respuesta: {respuesta}\n")
                print("-" * 60)
                
            except KeyboardInterrupt:
                print("\n\n👋 Sesión interrumpida. ¡Hasta luego!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")


def main():
    """Función principal."""
    agente = AgentePreguntas()
    agente.iniciar_sesion_interactiva()


if __name__ == "__main__":
    main()
