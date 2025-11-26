import os
import sys
import requests
from dotenv import load_dotenv
import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='langchain_core._api.deprecation')

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.chat_history import InMemoryChatMessageHistory, BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.tools import tool
from langchain_community.vectorstores import FAISS

API_URL = "http://localhost:5000"

os.environ["LANGCHAIN_TRACING"] = "false"
os.environ["LANGSMITH_TRACING"] = "false"

load_dotenv()

@tool
def consultar_informacion_clinica(consulta: str) -> str:
    """Busca información odontológica en el índice FAISS local."""
    try:
        embeddings = OpenAIEmbeddings(
            azure_endpoint=os.getenv('OPENAI_BASE_URL'),
            api_key=os.getenv('OPENAI_API_KEY'),
            azure_deployment=os.getenv('DEPLOYMENT_NAME')
        )
        db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        retriever = db.as_retriever(search_kwargs={"k": 3})
        docs = retriever.invoke(consulta)
        contexto = "\n---\n".join([doc.page_content for doc in docs])
        return contexto if contexto else "No se encontró información relevante."
    except Exception as e:
        return f"Error en RAG: {e}"

chat_history_store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in chat_history_store:
        chat_history_store[session_id] = InMemoryChatMessageHistory()
    return chat_history_store[session_id]

class DentalChatbot:

    def __init__(self):
        self.llm = None
        self.agent_with_history = None
        self.tools = [consultar_informacion_clinica]
        self.verificar_api()
        self.setup_chatbot()

    def verificar_api(self):
        try:
            r = requests.get(f"{API_URL}/api/health", timeout=1)
            if r.status_code == 200:
                print("✓ API Flask conectada correctamente.")
            else:
                print("⚠ API Flask responde pero no correctamente.")
        except:
            print("⚠ No se pudo conectar con la API Flask en http://localhost:5000")

    def registrar_consulta_api(self, pregunta: str):
        try:
            requests.post(
                f"{API_URL}/api/registrar_consulta",
                json={"pregunta": pregunta},
                timeout=1
            )
        except:
            print("⚠ No se pudo registrar la consulta en la API Flask.")

    def setup_chatbot(self):
        try:
            print("Inicializando modelo...")
            self.llm = ChatOpenAI(
                base_url=os.getenv('OPENAI_BASE_URL'),
                api_key=os.getenv('OPENAI_API_KEY'),
                model=os.getenv('DEPLOYMENT_NAME'),
                temperature=0.1
            )

            prompt = ChatPromptTemplate.from_messages([
                (
                    "system",
                    "Eres un asistente dental profesional de la Clínica Sonrisa Saludable. "
                    "Usa un tono profesional. Responde con precisión. Usa herramientas solo si es útil."
                ),
                ("placeholder", "{chat_history}"),
                ("human", "{input}")
            ])

            chain = prompt | self.llm

            self.agent_with_history = RunnableWithMessageHistory(
                chain,
                get_session_history,
                input_messages_key="input",
                history_messages_key="chat_history"
            )

            print("✓ Agente listo.")
        except Exception as e:
            print(f"❌ Error configurando agente: {e}")

    def enviar_consulta(self, mensaje, session_id="default"):
        try:
            self.registrar_consulta_api(mensaje)
            respuesta = self.agent_with_history.invoke(
                {"input": mensaje},
                config={"configurable": {"session_id": session_id}}
            )
            return respuesta
        except Exception as e:
            return f"Error procesando consulta: {e}"

def main():
    print("🦷 Agente Dental con RAG + Flask API\n")

    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Falta API KEY en .env")
        sys.exit(1)

    chatbot = DentalChatbot()
    session_id = "sesion_principal"

    while True:
        pregunta = input("\n👤 Paciente: ").strip()

        if pregunta.lower() in ["salir", "exit", "quit"]:
            print("Adiós.")
            break

        respuesta = chatbot.enviar_consulta(pregunta, session_id)
        print("🤖 Asistente:", respuesta)

if __name__ == "__main__":
    main()
