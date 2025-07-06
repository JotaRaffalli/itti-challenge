# ITTI Technical Test - Prompt Engineering Implementation

## Descripción

Monorepo que contiene una implementación de prompt engineering para un chatbot financiero, desarrollado con FastAPI, LangChain y OpenAI GPT-3.5-turbo. Incluye sistema de evaluación automatizada y métricas de calidad.

## Arquitectura

El proyecto está organizado como un monorepo Nx con las siguientes aplicaciones:

- **`apps/itti-backend`**: API FastAPI con prompt engineering y evaluación automatizada
- **`apps/sample-chat-app`**: Frontend React para demo del chatbot
- **`notebooks/data-analysis`**: Jupyter notebook con defensa técnica y análisis

## Instalación

### Prerrequisitos

- Node.js 18+
- Python 3.11+
- OpenAI API Key

### Setup

```bash
# Instalar dependencias del monorepo
npm install

# Configurar backend
cd apps/itti-backend
cp .env.example .env
nx install itti-backend
```

## Comandos Nx

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

## Evaluación del Sistema

```bash
# Ejecutar evaluación automatizada
cd apps/itti-backend
python run_evaluation.py
```

## Defensa Técnica

La defensa técnica completa del proyecto se encuentra en:
[`notebooks/data-analysis/challenge-genai-20250610.ipynb`](notebooks/data-analysis/challenge-genai-20250610.ipynb)

Este notebook incluye:
- Análisis de técnicas de prompt engineering implementadas
- Proceso de desarrollo y decisiones de diseño
- Evaluación de resultados y métricas
- Conclusiones técnicas

```bash
# En otra terminal, ejecutar evaluación completa
cd apps/itti-backend
python run_evaluation.py
```

### 3. **Acceder a Interfaces**

- **API Swagger**: http://localhost:8000/docs
- **Dashboard**: http://localhost:8000/dashboard
- **Health Check**: http://localhost:8000/api/chat/health

### 4. **Demo Frontend (Opcional)**

```bash
# En otra terminal
nx serve sample-chat-app
# Abrir navegador en http://localhost:4200
```

---

## 🧪 **Comandos Nx Disponibles**

### **Backend (FastAPI)**
```bash
nx serve itti-backend        # Iniciar servidor de desarrollo
nx test itti-backend         # Ejecutar tests unitarios
nx lint itti-backend         # Linting del código Python
```

### **Frontend (React)**
```bash
nx serve sample-chat-app     # Iniciar servidor de desarrollo
nx build sample-chat-app     # Build de producción
nx test sample-chat-app      # Ejecutar tests Jest
nx e2e sample-chat-app-e2e   # Tests end-to-end con Playwright
```

### **Notebooks (Jupyter)**
```bash
nx jupyter data-analysis     # Abrir Jupyter Lab
```

### **Comandos Globales**
```bash
nx run-many -t test          # Ejecutar todos los tests
nx run-many -t lint          # Linting de todos los proyectos
nx graph                     # Visualizar dependencias del monorepo
```

---

## 🛠️ **Stack Tecnológico**

### **Backend & AI**
- **FastAPI**: Framework web moderno para Python APIs
- **LangChain**: Framework para aplicaciones LLM empresariales
- **OpenAI GPT-3.5-turbo**: Modelo de lenguaje de última generación
- **Pydantic**: Validación de datos y modelado con tipos
- **SentenceTransformers**: Embeddings para similaridad semántica
- **UV**: Gestor de paquetes Python de alta performance

### **Frontend & Testing**
- **React + Vite**: Framework frontend moderno con TypeScript
- **Playwright**: Testing end-to-end automatizado
- **Jest**: Framework de testing unitario

### **DevOps & Monorepo**
- **Nx**: Herramientas avanzadas de monorepo y build system
- **Jupyter**: Notebooks interactivos para análisis de datos
- **ESLint + Prettier**: Linting y formateo automático

---

## **Métricas de Calidad**

### **Performance del Sistema**
- **Intent Accuracy**: 100% (15/15 consultas correctas)
- **Product Detection**: 100% (15/15 productos identificados)
- **Semantic Similarity**: 83.5% promedio con respuestas esperadas
- **Average Response Time**: ~1.2 segundos
- **Confidence Score**: 0.97 promedio

### **Métricas de Experiencia**
- **Empathy Score**: ~92% (indicadores de lenguaje empático)
- **Clarity Score**: ~88% (estructura y claridad de respuestas)
- **Actionability**: ~95% (presencia de próximos pasos)

---

## **Técnicas de Prompt Engineering Implementadas**

### ✅ **Few-Shot Learning**
3 ejemplos estratégicos que cubren diferentes tipos de consultas financieras

### ✅ **Structured Output**
JSON Schema con validación estricta usando Pydantic

### ✅ **Role-Based Prompting**
Personalidad definida (Álex) con límites profesionales claros

### ✅ **Chain-of-Thought**
Instrucciones que fuerzan razonamiento interno del modelo

### ✅ **In-Context Learning**
Información de productos financieros embebida en el prompt

---

## **Casos de Uso Evaluados**

### **Dataset Básico (8 consultas)**
1. Beneficios de tarjeta de débito ✅
2. Requisitos para préstamo ✅
3. Tasas de interés tarjeta de crédito ✅
4. Proceso de solicitud ✅
5. Comparación de productos ✅
6. Beneficios específicos de crédito ✅
7. Pregunta fuera de contexto ✅
8. Requisitos con historial crediticio negativo ✅

### **Casos Edge (7 consultas adicionales)**
- Consultas sobre múltiples productos
- Preguntas ambiguas que requieren clarificación
- Casos de seguridad (robo de tarjeta)
- Consultas de estudiantes
- Preguntas completamente fuera del dominio

