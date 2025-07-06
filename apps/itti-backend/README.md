# ITTI Backend - Prompt Engineering API

## Descripción

API desarrollada en FastAPI para un chatbot financiero que implementa técnicas de prompt engineering. Utiliza LangChain como orquestador y Google Gemini como modelo de lenguaje principal. El sistema incluye un framework de evaluación automatizada que mide métricas de precisión y calidad de respuesta.

## Instalación

### Prerrequisitos

- Python 3.11+
- Una Google API Key

### Setup

1.  **Configurar variables de entorno:**
    Desde la raíz del monorepo, crea una copia del archivo de ejemplo:
    ```bash
    cp apps/itti-backend/.env.example apps/itti-backend/.env
    ```
    A continuación, edita el archivo `apps/itti-backend/.env` y añade tu `GOOGLE_API_KEY`.

2.  **Instalar dependencias:**
    Desde la raíz del monorepo, ejecuta el siguiente comando para instalar las dependencias del proyecto:
    ```bash
    nx install itti-backend
    ```

## Ejecución

### Servidor de Desarrollo

Para iniciar el servidor en modo de desarrollo, que se recarga automáticamente con los cambios, ejecuta:
```bash
nx serve itti-backend
```
El servidor estará disponible en `http://localhost:8000`.

### Evaluación Automatizada

Para ejecutar el script que evalúa el sistema contra el dataset de pruebas, asegúrate de que el servidor esté corriendo y luego ejecuta:
```bash
python apps/itti-backend/run_evaluation.py
```

## Endpoints Principales

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `POST` | `/chat/process` | Procesa una consulta de un usuario y devuelve la respuesta del chatbot. |
| `POST` | `/evaluation/run-full-dataset`| Ejecuta la evaluación completa del sistema contra el dataset definido. |
| `GET` | `/docs` | Ofrece la documentación interactiva de la API (Swagger UI). |

## Arquitectura

-   **`main.py`**: Punto de entrada de la API con la definición de los endpoints de FastAPI.
-   **`services/`**: Contiene la lógica de negocio desacoplada.
    -   **`prompt_service.py`**: Se encarga de la construcción y gestión de los prompts dinámicos.
    -   **`llm_service.py`**: Actúa como interfaz con el LLM a través de LangChain.
    -   **`comprehensive_evaluator.py`**: Implementa el sistema de evaluación con métricas de calidad.
-   **`models/`**: Define los modelos Pydantic para la validación estricta de los datos de entrada y salida.
-   **`prompts/`**: Almacena las plantillas de los prompts en formato XML.
-   **`data/`**: Contiene los datasets utilizados para la evaluación del sistema.
