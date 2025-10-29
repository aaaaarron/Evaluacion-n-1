import os
import sys
from dotenv import load_dotenv

# Para compatibilidad con Python 3.14
import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='langchain_core._api.deprecation')

# --- Importaciones de LangChain ---
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.chat_history import InMemoryChatMessageHistory, BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.tools import tool
from langchain_core.output_parsers import JsonOutputParser
from langchain_community.vectorstores import FAISS

# --- Configuración Inicial ---
# Deshabilitar LangSmith (opcional)
os.environ["LANGCHAIN_TRACING"] = "false"
os.environ["LANGSMITH_TRACING"] = "false"

# Cargar variables de entorno (desde .env)
load_dotenv()


# --- HERRAMIENTA DE CONSULTA (RAG) ---
@tool
def consultar_informacion_clinica(consulta: str) -> str:
    """
    Útil para responder preguntas sobre información de la Clínica "Sonrisa Saludable".
    Busca información sobre horarios, precios de servicios, seguros aceptados,
    teléfonos, dirección y protocolos de la clínica.
    """
    print(f"\n[Herramienta RAG]: Recibida consulta: '{consulta}'")
    try:
        # 1. Cargar el modelo de embeddings
        embeddings = OpenAIEmbeddings(
            azure_endpoint=os.getenv('OPENAI_BASE_URL'),
            api_key=os.getenv('OPENAI_API_KEY'),
            azure_deployment=os.getenv('DEPLOYMENT_NAME')
        )
        
        # 2. Cargar la base de datos vectorial local
        db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        
        # 3. Crear un "retriever" para buscar
        retriever = db.as_retriever(search_kwargs={"k": 3}) # k=3 trae los 3 chunks más relevantes
        
        # 4. Buscar documentos relevantes
        docs = retriever.invoke(consulta)
        
        # 5. Formatear la respuesta
        contexto = "\n---\n".join([doc.page_content for doc in docs])
        print(f"[Herramienta RAG]: Contexto encontrado:\n{contexto}")
        
        return contexto
    
    except Exception as e:
        print(f"[Herramienta RAG]: Error: {e}")
        return "Error al consultar la base de conocimiento. Verifica que el índice 'faiss_index' exista."

# --- CONFIGURACIÓN DE MEMORIA DE CORTO PLAZO ---
# Usamos un diccionario simple para guardar el historial de chat en memoria RAM
chat_history_store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """Obtiene el historial de chat para una sesión dada."""
    if session_id not in chat_history_store:
        chat_history_store[session_id] = InMemoryChatMessageHistory()
    return chat_history_store[session_id]


# --- CLASE PRINCIPAL DEL AGENTE ---
class DentalChatbot:
    def __init__(self):
        self.llm = None
        self.agent_with_history = None
        # Lista de herramientas que el agente puede usar
        self.tools = [consultar_informacion_clinica]
        self.setup_chatbot()
    
    def setup_chatbot(self):
        """Configura el Agente dental con LangChain"""
        try:
            print("🔄 Inicializando modelo GitHub Models (Azure AI)...")
            
            # 1. Configurar el LLM
            self.llm = ChatOpenAI(
                base_url=os.getenv('OPENAI_BASE_URL'),
                api_key=os.getenv('OPENAI_API_KEY'),
                model=os.getenv('DEPLOYMENT_NAME'),
                temperature=0.1
            )
            
            # 2. Definir el NUEVO prompt del sistema para el AGENTE
            prompt = ChatPromptTemplate.from_messages([
                ("system", """Eres un asistente dental profesional de la Clínica "Sonrisa Saludable".
- Mantén un tono profesional pero empático.
- No des diagnósticos médicos complejos.
- Para situaciones de emergencia, deriva inmediatamente al teléfono de urgencias.
- Utiliza tus herramientas para responder preguntas sobre la clínica (precios, horarios, etc.)
- Tienes acceso a un historial de chat para mantener el contexto."""),
                ("placeholder", "{chat_history}"),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}")
            ])
            
            # 3. Crear el Agente usando RunnableWithMessageHistory directamente
            chain = prompt | self.llm | JsonOutputParser()
            self.agent_with_history = RunnableWithMessageHistory(
                chain,
                get_session_history,
                input_messages_key="input",
                history_messages_key="chat_history"
            )
            
            # El agente ya está inicializado con initialize_agent
            
            print("✅ Agente LangChain configurado correctamente")
            
        except Exception as e:
            print(f"❌ Error en configuración: {e}")
            print("\n🔧 Solución: Asegúrate de que:")
            print("1. El archivo .env está configurado correctamente")
            print("2. Las credenciales de GitHub Models son válidas")
            print("3. El modelo especificado está disponible")
            print("4. El índice 'faiss_index' existe en la carpeta")

    def enviar_consulta(self, mensaje, session_id="usuario_123"):
        """Envía una consulta al agente"""
        try:
            if not self.agent_with_history:
                return "Sistema no configurado correctamente."
            
            # Invocar al agente con el historial
            respuesta = self.agent_with_history.invoke(
                {"input": mensaje},
                config={"configurable": {"session_id": session_id}}
            )
            
            # La respuesta del agente está en la clave 'output'
            return respuesta.get('output', 'No se obtuvo respuesta.')
            
        except Exception as e:
            return f"Error al procesar la consulta: {e}"

# --- FUNCIÓN PRINCIPAL DE EJECUCIÓN ---
def main():
    print("🦷 CLÍNICA DENTAL 'SONRISA SALUDABLE'")
    print("🤖 Agente Virtual (v2) con LangChain + Herramientas")
    print("=" * 60)
    
    # Verificar variables de entorno (simplificado)
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ Faltan variables de entorno. Revisa tu .env")
        sys.exit(1)
    
    print("✅ Variables de entorno cargadas")
    
    # Inicializar chatbot (ahora es un agente)
    chatbot = DentalChatbot()
    
    if not chatbot.agent_with_history:
        print("❌ No se pudo inicializar el agente.")
        return
    
    print("\n💬 ¡Sistema listo para conversar!")
    print("📋 Puedes preguntar sobre: horarios, teléfonos, seguros, precios...")
    print("❌ Escribe 'salir' para terminar")
    print("-" * 60)
    
    # Bucle principal de conversación
    session_id = "conversacion_principal"
    
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
            respuesta = chatbot.enviar_consulta(consulta, session_id)
            print(respuesta)
            
        except KeyboardInterrupt:
            print("\n\n¡Hasta pronto! 👋")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

# --- PUNTO DE ENTRADA DEL SCRIPT ---
if __name__ == "__main__":
    main()