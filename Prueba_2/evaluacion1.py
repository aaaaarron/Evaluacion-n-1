# evaluacion1.py
import os
import sys
from dotenv import load_dotenv

# Disable LangSmith tracking
os.environ["LANGCHAIN_TRACING"] = "false"
os.environ["LANGSMITH_TRACING"] = "false"

# Load environment variables
load_dotenv()

# Verificar e instalar dependencias si es necesario
try:
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import PromptTemplate
    from langchain_core.chat_history import InMemoryChatMessageHistory
    from langchain_core.runnables.history import RunnableWithMessageHistory
except ImportError as e:
    print("❌ Faltan dependencias. Instalando...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "langchain-openai", "python-dotenv", "langchain-core"])
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import PromptTemplate
    from langchain_core.chat_history import InMemoryChatMessageHistory
    from langchain_core.runnables.history import RunnableWithMessageHistory

class DentalChatbot:
    def __init__(self):
        self.llm = None
        self.chat_history = None
        self.conversation_chain = None
        self.setup_chatbot()
    
    def setup_chatbot(self):
        """Configura el chatbot con LangChain"""
        try:
            print("🔄 Inicializando modelo GitHub Models (Azure AI)...")
            
            # Configurar GitHub Models (Azure AI) con ChatOpenAI
            self.llm = ChatOpenAI(
                base_url=os.getenv('OPENAI_BASE_URL'),
                api_key=os.getenv('OPENAI_API_KEY'),
                model=os.getenv('DEPLOYMENT_NAME'),
                temperature=0.1
            )
            
            # Template de prompt especializado para dental
            prompt_template = PromptTemplate(
                input_variables=["input"],
                template="""Eres un asistente dental profesional de la Clínica "Sonrisa Saludable".

INFORMACIÓN OFICIAL DE LA CLÍNICA:
- **Horarios de atención**: Lunes a Viernes: 9:00 - 19:00 hrs, Sábados: 10:00 - 14:00 hrs
- **Teléfonos**: Central: (2) 2345 6789, WhatsApp: +56 9 1234 5678, Urgencias: +56 9 8765 4321
- **Seguros de salud aceptados**: Fonasa (todos los tramos), Isapres: Banmédica, Colmena, Cruz Blanca, Consalud
- **Dirección**: Avenida Dental 123, Santiago Centro
- **Servicios principales**: 
  * Consulta general: $15.000
  * Limpieza dental: $25.000
  * Obturaciones (tapaduras): $20.000 - $35.000
  * Blanqueamiento dental: $120.000
  * Ortodoncia: evaluación inicial $30.000

PROTOCOLOS IMPORTANTES:
- Para emergencias dentales, contactar inmediatamente por teléfono
- Después de una extracción: reposo, dieta blanda, no fumar por 48 horas
- Cita de control post-tratamiento a los 7 días

INSTRUCCIONES PARA EL ASISTENTE:
1. Responde ÚNICAMENTE con la información proporcionada arriba
2. Mantén un tono profesional pero empático
3. No des diagnósticos médicos complejos
4. Para situaciones de emergencia, deriva inmediatamente al teléfono de urgencias
5. Si la consulta no está en la información, sugiere contactar directamente con la clínica

Consulta del paciente: {input}

Respuesta del Asistente Dental:"""
            )
            
            # Crear la cadena simple con el nuevo formato
            self.conversation_chain = prompt_template | self.llm
            
            print("✅ Sistema LangChain configurado correctamente")
            
        except Exception as e:
            print(f"❌ Error en configuración: {e}")
            print("\n🔧 Solución: Asegúrate de que:")
            print("1. El archivo .env está configurado correctamente")
            print("2. Las credenciales de GitHub Models son válidas")
            print("3. El modelo especificado está disponible")

    def enviar_consulta(self, mensaje):
        """Envía una consulta al chatbot"""
        try:
            if not self.conversation_chain:
                return "Sistema no configurado correctamente."
            
            # Usar la cadena simple sin historial por ahora para evitar complejidad
            respuesta = self.conversation_chain.invoke({"input": mensaje})
            
            # Extraer el contenido de la respuesta
            if hasattr(respuesta, 'content'):
                return respuesta.content
            else:
                return str(respuesta)
            
        except Exception as e:
            return f"Error al procesar la consulta: {e}"

    def _format_response(self, query: str, info: dict) -> str:
        """Formatea la respuesta basada en la información recuperada"""
        query = query.lower()
        
        # Respuestas específicas para servicios
        if "limpieza" in query:
            return f"El precio de la limpieza dental es: ${info['servicios']['limpieza_dental']}"
        
        if "general" in query or "consulta general" in query:
            return f"El precio de la consulta general es: ${info['servicios']['consulta_general']}"
            
        if "obturacion" in query or "tapaduras" in query:
            return f"El precio de las obturaciones va desde ${info['servicios']['obturaciones']['desde']} hasta ${info['servicios']['obturaciones']['hasta']}"
            
        if "blanqueamiento" in query:
            return f"El precio del blanqueamiento dental es: ${info['servicios']['blanqueamiento']}"
            
        if "ortodoncia" in query:
            return f"El precio de la evaluación de ortodoncia es: ${info['servicios']['ortodoncia_evaluacion']}"

        # Respuestas específicas para seguros
        seguros_especificos = {
            "fonasa": "Sí, trabajamos con Fonasa",
            "banmedica": "Sí, trabajamos con Banmédica",
            "colmena": "Sí, trabajamos con Colmena",
            "cruz blanca": "Sí, trabajamos con Cruz Blanca",
            "consalud": "Sí, trabajamos con Consalud"
        }
        
        for seguro, respuesta in seguros_especificos.items():
            if seguro in query:
                return respuesta

        # Respuestas generales originales
        if "horario" in query:
            return f"Nuestros horarios de atención son:\n- Lunes a Viernes: {info['horarios']['lunes_viernes']}\n- Sábados: {info['horarios']['sabados']}"
        
        if any(word in query for word in ["precio", "valor", "costo"]):
            services = info['servicios']
            return f"Estos son nuestros precios:\n- Consulta general: ${services['consulta_general']}\n- Limpieza dental: ${services['limpieza_dental']}\n- Obturaciones: ${services['obturaciones']['desde']} - ${services['obturaciones']['hasta']}"
        
        if "seguro" in query:
            return f"Trabajamos con los siguientes seguros: {', '.join(info['seguros'])}"
        
        if any(word in query for word in ["teléfono", "contacto", "número"]):
            contact = info['contacto']
            return f"Puedes contactarnos en:\n- Teléfono: {contact['telefono']}\n- WhatsApp: {contact['whatsapp']}\n- Urgencias: {contact['urgencias']}"
        
        return "Lo siento, no pude entender tu consulta. ¿Podrías reformularla?"

def verify_connections():
    """Verifica las conexiones y dependencias"""
    try:
        # Verificar variables de entorno
        required_env_vars = [
            'OPENAI_BASE_URL',
            'OPENAI_API_KEY',
            'DEPLOYMENT_NAME'
        ]
        
        missing_vars = [var for var in required_env_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"Faltan variables de entorno: {', '.join(missing_vars)}")
            
        print("✅ Variables de entorno verificadas")
        return True
        
    except Exception as e:
        print(f"❌ Error en la verificación: {e}")
        return False

def main():
    print("🦷 CLÍNICA DENTAL 'SONRISA SALUDABLE'")
    print("🤖 Asistente Virtual con LangChain + GitHub Models")
    print("=" * 60)
    
    # Verificar conexiones antes de inicializar el chatbot
    if not verify_connections():
        print("❌ Error en la configuración inicial")
        sys.exit(1)
    
    # Inicializar chatbot
    chatbot = DentalChatbot()
    
    if not chatbot.conversation_chain:
        print("No se pudo inicializar el chatbot.")
        return
    
    print("\n💬 ¡Sistema listo para conversar!")
    print("📋 Puedes preguntar sobre: horarios, teléfonos, seguros, precios, protocolos")
    print("❌ Escribe 'salir' para terminar")
    print("-" * 60)
    
    # Bucle principal de conversación
    while True:
        try:
            consulta = input("\n👤 Paciente: ").strip()
            
            if consulta.lower() in ['salir', 'exit', 'quit']:
                print("¡Gracias por preferir Sonrisa Saludable! 😊")
                break
                
            if not consulta:
                continue
            
            # Obtener respuesta
            print("🤖 Asistente: ", end="", flush=True)
            respuesta = chatbot.enviar_consulta(consulta)
            print(respuesta)
            
        except KeyboardInterrupt:
            print("\n\n¡Hasta pronto! 👋")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()