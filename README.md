# ITTI Technical Test - Prompt Engineering Implementation

## Descripción

Monorepo que contiene una implementación de:
- Prompt engineering para un chatbot financiero, desarrollado con FastAPI y LangChain. Incluye sistema de evaluación automatizada y métricas de calidad.
- Agentes especializados en la atención de requerimientos de VuelaConNosotros usando Langraph, segmentando la responsabilidad de cada paso en Nodos y guardando datos relevantes en un estado. 

## Arquitectura

El proyecto está organizado como un monorepo Nx con las siguientes aplicaciones:

- **`apps/itti-backend`**: API FastAPI con la prueba de concepto del challenge.
- **`notebooks/data-analysis`**: Jupyter notebook con defensa técnica y análisis

## Instalación

### Prerrequisitos

- Node.js 18+
- Python 3.11+
- Api key de Gemini o OpenAI

### Setup

```bash
# Instalar dependencias del monorepo
npm install

# Configurar backend
cd apps/itti-backend
cp .env.example .env
nx install itti-backend
```

Despues levantar el servidor con:

```bash
nx serve itti-backend
```

## Cómo probar el sistema?

He estructurado la API para que cada parte del challenge sea atendida por endpoints específicos y pueda ser probada con su propio script de evaluación.

### Parte 1: Agente Financiero (Prompt Engineering)

Esta parte corresponde al chatbot financiero. La evaluación se realiza a través de un script que consume un endpoint dedicado.

- **Script de prueba automatizada:**
  ```bash
  # Desde la raíz del monorepo, ejecuta:
  cd apps/itti-backend && python run_evaluation.py
  ```
- **Endpoint principal:** `POST /evaluation/run-full-dataset`

### Parte 2: Agente de Viajes (Arquitectura Multi-Agente con LangGraph)

Esta parte corresponde al sistema "VuelaConNosotros", implementado con una arquitectura de agentes especializados.

- **Script de prueba automatizada:**
  ```bash
  # Desde la raíz del monorepo, ejecuta:
  cd apps/itti-backend && python test_app.py
  ```
- **Endpoint principal:** `POST /vuelaconnosotros/chat`

## Defensa Técnica

La defensa técnica completa del proyecto se encuentra en:
- [`notebooks/data-analysis/defensa_prompt_engineering.ipynb`](notebooks/data-analysis/defensa_prompt_engineering.ipynb)

- [`notebooks/data-analysis/defensa-arquitectura-cognitiva.ipynb`](notebooks/data-analysis/defensa-arquitectura-cognitiva.ipynb)


## Otros Comandos de Nx 

```bash
# Listar proyectos disponibles
nx show projects

# Ejecutar backend
nx serve itti-backend

# Ejecutar frontend
nx serve sample-chat-app

# Ejecutar tests
nx test itti-backend

# Build para producción
nx build itti-backend
```
