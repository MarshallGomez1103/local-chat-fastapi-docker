# Chat Local con FastAPI + Docker + SQLite

Aplicación web que recibe un mensaje, consulta un modelo local compatible con OpenAI API, guarda el historial en SQLite y devuelve la respuesta en una interfaz web.

## Qué hace este proyecto

- Recibe mensajes desde una interfaz web o por query params
- Consulta un backend de IA local
- Guarda cada pregunta y respuesta en SQLite
- Muestra el historial en pantalla
- Se ejecuta con Docker Compose

## Arquitectura

Navegador -> FastAPI en Docker -> backend local de IA (LM Studio / Ollama) -> SQLite

## Importante

Este proyecto **no incluye el modelo dentro del contenedor**.

El contenedor solo ejecuta:

- FastAPI
- la interfaz web
- la lógica de conexión
- SQLite

El modelo debe estar corriendo localmente en el computador host usando un backend compatible, por ejemplo:

- **LM Studio**
- **Ollama**

## Requisitos

- Docker Desktop instalado y encendido
- Git instalado
- Un backend local de IA corriendo en el host:
    - LM Studio
    - o Ollama

---

## 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd chat_app
```

---

## 2. Configuración del backend local

El proyecto usa estas variables:

- `MODEL_BASE_URL`: URL del backend local
- `MODEL_API_KEY`: valor requerido por el cliente OpenAI
- `MODEL_NAME`: nombre del modelo cargado
- `DATABASE_URL`: ruta de SQLite

El proyecto trae valores por defecto para **LM Studio**, pero se puede cambiar fácilmente para **Ollama**.

### Opción A: usar LM Studio

Ejemplo típico:

```env
MODEL_BASE_URL=http://host.docker.internal:1234/v1
MODEL_API_KEY=lm-studio
MODEL_NAME=openai/gpt-oss-20b
DATABASE_URL=sqlite:///./data/chat.db
