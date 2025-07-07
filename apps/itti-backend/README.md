# ITTI Backend - API de IA Conversacional

## Descripción

He desarrollado esta API en FastAPI para demostrar dos soluciones de IA conversacional, atendiendo a los dos retos técnicos propuestos:

1.  **Chatbot Financiero (Challenge 1):** Implementa técnicas avanzadas de prompt engineering y un sistema de evaluación automatizada para un asistente bancario.
2.  **Asistente de Viajes "VuelaConNosotros" (Challenge 2):** Despliega una arquitectura multi-agente con LangGraph para gestionar tareas complejas como consultas de vuelos y cambios de reserva.

Utiliza LangChain como orquestador y puede conectarse a Google Gemini o a OpenAI.

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

### Pruebas Automatizadas

He implementado scripts para probar cada parte del challenge de forma independiente. Asegúrate de que el servidor esté corriendo antes de ejecutarlos.

**1. Evaluación del Agente Financiero (Challenge 1):**
```bash
# Desde la raíz del monorepo, ejecuta:
python apps/itti-backend/run_evaluation.py
```

**2. Evaluación del Asistente de Viajes (Challenge 2):**
```bash
# Desde la raíz del monorepo, ejecuta:
python apps/itti-backend/test_app.py
```

## Endpoints Principales

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `POST` | `/evaluation/run-full-dataset`| Ejecuta la evaluación completa del agente financiero. |
| `POST` | `/vuelaconnosotros/chat` | Procesa una consulta para el asistente de viajes multi-agente. |
| `GET` | `/docs` | Ofrece la documentación interactiva de la API (Swagger UI). |

## Arquitectura

-   **`main.py`**: Punto de entrada de la API con la definición de los endpoints de FastAPI.
-   **`api/`**: Define los routers para cada funcionalidad.
    -   **`chatbot_routes.py`**: Rutas para el asistente de viajes "VuelaConNosotros".
-   **`services/`**: Contiene la lógica de negocio desacoplada.
    -   **`prompt_service.py`**: Construcción y gestión de los prompts dinámicos (Challenge 1).
    -   **`comprehensive_evaluator.py`**: Sistema de evaluación con métricas de calidad (Challenge 1).
    -   **`chatbot_service.py`**: Orquesta la lógica del asistente de viajes (Challenge 2).
    -   **`llm_service.py`**: Interfaz con el LLM a través de LangChain.
-   **`agents/`**: Contiene los agentes especializados para el asistente de viajes (Challenge 2).
-   **`orchestrator/`**: Define el grafo de LangGraph que estructura la conversación (Challenge 2).
-   **`models/`**: Define los modelos Pydantic para la validación estricta de los datos.
-   **`prompts/`**: Almacena las plantillas de los prompts en formato XML.
-   **`data/`**: Contiene los datasets utilizados para la evaluación.
