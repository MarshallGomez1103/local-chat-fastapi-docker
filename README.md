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