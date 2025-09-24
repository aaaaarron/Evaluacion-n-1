# Asistente Virtual para Clínica Dental "Sonrisa Saludable"

## Descripción

Este proyecto implementa un sistema de asistente virtual automatizado para la atención al cliente de una clínica dental. El sistema utiliza tecnologías de procesamiento de lenguaje natural para proporcionar información precisa sobre servicios, horarios, precios y procedimientos de la clínica.

## Tecnologías Utilizadas

- Python 3.8+
- LangChain - Framework para desarrollo de aplicaciones con modelos de lenguaje
- OpenAI API - Servicios de procesamiento de lenguaje
- GitHub Models - Plataforma de modelos como servicio
- Python-dotenv - Gestión de variables de entorno

## Instalación

### Prerrequisitos

- Python 3.8 o superior instalado
- Cuenta de GitHub con acceso a GitHub Models
- Token de acceso personal de GitHub

### Pasos de Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   git clone [URL_del_repositorio]
   cd sonrisa-saludable-chatbot
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar variables de entorno**
   
   Crear un archivo `.env` en la raíz del proyecto con el siguiente contenido:
   ```
   OPENAI_BASE_URL=https://models.inference.ai.azure.com
   OPENAI_API_KEY=tu_token_de_github_aqui
   DEPLOYMENT_NAME=gpt-4o-mini
   LANGCHAIN_TRACING=false
   LANGSMITH_TRACING=false
   ```

### Obtención del Token de GitHub

Para obtener el token de acceso necesario:

1. Ir a GitHub.com e iniciar sesión
2. Navegar a Settings → Developer settings → Personal access tokens → Tokens (classic)
3. Hacer clic en "Generate new token (classic)"
4. Seleccionar los scopes necesarios para GitHub Models
5. Copiar el token generado y reemplazar `tu_token_de_github_aqui` en el archivo `.env`

**Importante**: Mantener el token seguro y no compartirlo públicamente.

## Ejecución

Para iniciar el asistente virtual:

```bash
python evaluacion1.py
```

El sistema se iniciará y estará listo para responder consultas sobre la clínica dental.

## Uso

El asistente puede responder preguntas sobre:
- Horarios de atención
- Precios de servicios
- Información de contacto
- Seguros aceptados
- Procedimientos y protocolos

Para salir del sistema, escribir: `salir`, `exit` o `quit`
