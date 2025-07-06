# ITTI Backend - Prompt Engineering Challenge

## 🎯 Descripción

Backend FastAPI que implementa la **Parte 1** del challenge de prompt engineering para un bot fintech, usando **LangChain + OpenAI GPT** con evaluación automatizada.

## 📋 Defensa Técnica Completa

> **Documento principal**: [`../../notebooks/data-analysis/challenge-genai-20250610.ipynb`](../../notebooks/data-analysis/challenge-genai-20250610.ipynb)

Este notebook contiene la defensa técnica completa con:

- ✅ Explicación detallada de técnicas de prompt engineering
- ✅ Dataset de evaluación y metodología
- ✅ Análisis crítico de resultados
- ✅ Instrucciones para ejecutar pruebas

## ⚡ Ejecución Rápida

### 1. Configurar API Key

```bash
# Crear archivo .env
cp .env.example .env
# Editar .env con tu OPENAI_API_KEY
```

### 2. Instalar y ejecutar

```bash
# Instalar dependencias
pip install -e .

# Iniciar servidor
uvicorn itti_backend.main:app --reload

# En otra terminal, ejecutar demo completo
python test_demo.py
```

## 🧪 Demo Automático

El script `test_demo.py` ejecuta:

- ✅ **10 casos de prueba** del dataset de evaluación
- ✅ **Métricas automatizadas** (Estructura, Empatía, Detección, Confianza)
- ✅ **Análisis de rendimiento** con resultados detallados

```bash
python test_demo.py
```

## 📡 API Principal

#### Endpoint de Testing con Evaluación

```http
POST /prompt/test
Content-Type: application/json

{
    "message": "¿Cuáles son los beneficios de la tarjeta de crédito?",
    "include_evaluation": true
}
```

#### Respuesta con Métricas

```json
{
  "query": {...},
  "response": {
    "reasoning": "El cliente consulta sobre beneficios...",
    "answer": "La Tarjeta de Crédito ITTI ofrece...",
    "next_steps": "Te recomiendo contactar..."
  },
  "evaluation": {
    "structure_score": 0.95,
    "empathy_score": 0.88,
    "product_detection_score": 1.0,
    "confidence_score": 0.92,
    "total_score": 0.94
  }
}
```

## 🏗️ Arquitectura Técnica

- **FastAPI**: Framework web moderno
- **LangChain**: Orquestador de LLM
- **OpenAI GPT-3.5-turbo**: Modelo de lenguaje
- **Pydantic**: Validación de datos
- **Evaluator**: Sistema de métricas automáticas

## 📊 Estructura del Código

```
itti_backend/
├── main.py                    # API endpoints
├── services/
│   ├── prompt_service.py      # Prompt unificado + LangChain
│   └── evaluator.py           # Sistema de evaluación
├── models/
│   └── fintech_models.py      # Modelos Pydantic
└── data/
    └── evaluation_dataset.py  # Dataset de pruebas
```

## 📖 Documentación Completa

**Para la defensa técnica completa, metodología, análisis y conclusiones, revisar**:
[`../../notebooks/data-analysis/challenge-genai-20250610.ipynb`](../../notebooks/data-analysis/challenge-genai-20250610.ipynb)
