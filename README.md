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
git clone https://github.com/MarshallGomez1103/local-chat-fastapi-docker.git
cd local-chat-fastapi-docker
```

---

## 2. Antes de ejecutar el proyecto

Para que la aplicación funcione correctamente deben estar activos **dos procesos en segundo plano** en el computador:

- **Docker Desktop**
- **el backend local de IA** (LM Studio o Ollama)

Si alguno de estos procesos no está corriendo, el contenedor no podrá conectarse al modelo.

---

## 3. Configuración del backend local

El proyecto usa estas variables:

- `MODEL_BASE_URL`: URL del backend local
- `MODEL_API_KEY`: valor requerido por el cliente OpenAI
- `MODEL_NAME`: nombre del modelo cargado
- `DATABASE_URL`: ruta de SQLite

El proyecto trae valores por defecto para **LM Studio**, pero se puede cambiar fácilmente para **Ollama** usando un archivo `.env`.

---

## Opción A: usar LM Studio

### 1. Abrir LM Studio

Abre **LM Studio** y carga el modelo que quieras usar.

### 2. Iniciar el servidor local de LM Studio

En una terminal ejecuta:

```powershell
$ lms server start --port 1234
```

Si todo está correcto deberías ver algo como:

```bash
$ lms server start --port 1234
Success! Server is now running on port 1234
```

Esto significa que LM Studio está exponiendo una API compatible con OpenAI en:

```
http://localhost:1234
```

### 3. Configuración típica para LM Studio

El proyecto ya trae valores por defecto compatibles con LM Studio:

```env
MODEL_BASE_URL=http://host.docker.internal:1234/v1
MODEL_API_KEY=lm-studio
MODEL_NAME=openai/gpt-oss-20b
DATABASE_URL=sqlite:///./data/chat.db
```

Normalmente **no es necesario crear un archivo `.env`** si usas LM Studio.

### 4. Verificar el modelo disponible

Puedes verificar qué modelos están cargados visitando:

```
http://localhost:1234/v1/models
```

El identificador que aparezca allí es el que debe usarse como `MODEL_NAME`.

---

## Opción B: usar Ollama

### 1. Instalar Ollama

Asegúrate de tener Ollama instalado en el sistema.

### 2. Descargar un modelo

Por ejemplo:

```bash
ollama pull llama3
```

### 3. Iniciar el servidor de Ollama

En una terminal ejecuta:

```bash
ollama serve
```

Esto inicia el servidor en:

```
http://localhost:11434
```

### 4. Verificar modelos disponibles

Puedes revisar los modelos instalados con:

```bash
ollama list
```

El nombre que aparezca es el que debe usarse como `MODEL_NAME`.

### 5. Crear archivo `.env`

Si vas a usar Ollama, crea un archivo `.env` en la raíz del proyecto con algo como esto:

```env
MODEL_BASE_URL=http://host.docker.internal:11434/v1
MODEL_API_KEY=ollama
MODEL_NAME=llama3
DATABASE_URL=sqlite:///./data/chat.db
```

---

## 4. Ejecutar la aplicación

Una vez que:

- Docker Desktop esté corriendo
- LM Studio **o** Ollama estén activos
- estés ubicado **dentro de la carpeta del proyecto**

ejecuta:

```bash
docker compose up --build
```

Este comando debe ejecutarse **dentro del directorio del proyecto**, donde se encuentra el archivo `docker-compose.yml`.

---

## 5. Abrir la aplicación

Cuando el contenedor termine de iniciar, abre en el navegador:

```
http://localhost:8000
```

También puedes probar los endpoints directamente:

```
http://localhost:8000/api/chat?message=hola
```

```
http://localhost:8000/api/history
```

---

## 6. Persistencia de datos

El historial de conversaciones se guarda en:

```
data/chat.db
```

Esto permite que los mensajes permanezcan guardados incluso si el contenedor se reinicia.

---

## 7. Detener la aplicación

Para detener el proyecto ejecuta:

```bash
docker compose down
```
