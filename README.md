# 🎯 ITTI Technical Test 2025

## 📋 Solución del Challenge de Prompt Engineering

Este repositorio contiene la solución completa para el challenge técnico de ITTI, enfocado en **prompt engineering** para un bot fintech.

### 🎯 **Defensa Técnica Principal**

📊 **[`notebooks/data-analysis/challenge-genai-20250610.ipynb`](notebooks/data-analysis/challenge-genai-20250610.ipynb)**

> Este notebook de Jupyter contiene la **defensa técnica completa** de la Parte 1 del challenge, incluyendo:
>
> - Explicación detallada de técnicas de prompt engineering aplicadas
> - Dataset de evaluación y metodología de testing
> - Instrucciones para ejecutar pruebas y evaluaciones
> - Análisis crítico de resultados y conclusiones
> - Mejoras avanzadas del system prompt con benchmarking

## 🏗️ Arquitectura

### Aplicaciones Principales:

- **Backend FastAPI** (`apps/itti-backend`): API de prompt engineering con LangChain + OpenAI
- **Demo Frontend** (`apps/sample-chat-app`): Interfaz de chat para testing (React + Vite)
- **Jupyter Notebooks** (`notebooks/data-analysis`): Análisis y defensa técnica

## 🛠️ Technologies Used

- **Nx**: Monorepo management and build orchestration
- **React**: Frontend framework with Vite bundler
- **FastAPI**: Modern Python web framework
- **UV**: Fast Python package manager
- **Jupyter**: Interactive notebooks for data science
- **TypeScript**: Type-safe JavaScript development
- **Ruff**: Python linting and formatting
- **ESLint**: JavaScript/TypeScript linting
- **Playwright**: End-to-end testing

## 🚀 Ejecutar la Solución

### 1. **Instalación de Dependencias**

```bash
# Instalar dependencias del monorepo
npm install

# Instalar dependencias del backend FastAPI
nx run itti-backend:install

# Instalar dependencias del notebook (opcional)
nx run data-analysis:install
```

### 2. **Configuración**

Crear archivo `.env` en `apps/itti-backend/`:

```env
OPENAI_API_KEY=tu_api_key_aqui
```

### 3. **Ejecutar Demo**

```bash
# Iniciar servidor FastAPI
nx serve itti-backend

# En otra terminal, ejecutar script de demo
cd apps/itti-backend
python test_demo.py
```

## 🎯 Comandos Principales

### Backend FastAPI (itti-backend)

```bash
# Servidor de desarrollo
nx serve itti-backend

# Servidor de producción
nx serve-prod itti-backend

# Build the backend
nx build itti-backend

# Run tests
nx test itti-backend

# Lint the code
nx lint itti-backend

# Format the code
nx format itti-backend

# Install dependencies
nx install itti-backend

# Evaluar respuestas
python -m itti_backend.services.evaluator

# Testing y linting
nx lint itti-backend
nx format itti-backend
```

### Jupyter Notebooks (data-analysis)

```bash
# Abrir notebook principal de defensa
nx jupyter data-analysis

# Convertir notebook a HTML
nx convert-notebooks data-analysis

# Linting de código Python
nx lint data-analysis
nx format data-analysis
```

### Otros Comandos Útiles

```bash
# Ver gráfico de dependencias del proyecto
nx graph

# Ejecutar comando en todos los proyectos
nx run-many -t lint

# Limpiar cache
nx reset
```

## 🔗 API Endpoints

El backend FastAPI expone los siguientes endpoints:

- `GET /`: Mensaje de bienvenida
- `GET /health`: Estado de salud de la API
- `POST /chat`: Endpoint principal para consultas fintech
- `POST /evaluate`: Evaluación de respuestas con métricas

### Ejemplo de Consulta

```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{
       "message": "Hello, how are you?",
       "user_id": "user123"
     }'
```

       "user": "¿Cuál es la diferencia entre una cuenta de ahorro y una cuenta corriente?",
       "context": "consulta_general"
     }'

````

## 🎮 Demo Completo

Para ejecutar la demostración completa del challenge:

1. **Iniciar servidor FastAPI**:
```bash
nx serve itti-backend
````

2. **Ejecutar script de demo** (en otra terminal):

```bash
cd apps/itti-backend
python test_demo.py
```

3. **Opcional - Interfaz React** (en otra terminal):

```bash
nx serve sample-chat-app
# Abrir navegador en http://localhost:4200
```

## 📊 Defensa Técnica

### � **Documento Principal**

La defensa técnica completa está en el notebook de Jupyter:
**[`notebooks/data-analysis/challenge-genai-20250610.ipynb`](notebooks/data-analysis/challenge-genai-20250610.ipynb)**

Para abrirlo:

```bash
nx jupyter data-analysis
```

### 🔍 **Contenido de la Defensa**

- ✅ **Explicación de técnicas de prompt engineering**
- ✅ **Dataset de evaluación y metodología**
- ✅ **Instrucciones para ejecutar pruebas**
- ✅ **Análisis crítico de resultados**
- ✅ **Mejoras avanzadas del system prompt**
- ✅ **Benchmarking de técnicas**

## 🛠️ Tecnologías Utilizadas

- **Nx**: Gestión del monorepo y orchestración
- **FastAPI**: Framework web moderno para Python
- **LangChain**: Framework para aplicaciones LLM
- **OpenAI GPT**: Modelo de lenguaje para generación
- **React + Vite**: Frontend moderno con TypeScript
- **Jupyter**: Notebooks interactivos para análisis
- **UV**: Gestor de paquetes Python rápido
- **Pydantic**: Validación de datos y modelado

## 🏗️ Estructura del Proyecto

```
├── apps/
│   ├── itti-backend/           # FastAPI application
│   ├── sample-chat-app/        # React application
│   └── sample-chat-app-e2e/    # E2E tests for React app
├── notebooks/
│   └── data-analysis/          # Jupyter notebooks project
├── libs/                       # Shared libraries (empty for now)
├── nx.json                     # Nx workspace configuration
├── package.json                # Node.js dependencies
└── README.md                   # This file
```

## 🔧 Development Workflow

1. **Create new libraries**: Use `nx g @nx/js:library my-lib` for shared TypeScript libraries
2. **Add Python dependencies**: Use `nx add project-name --args="package-name"`
3. **Run tests**: Use `nx test project-name` or `nx run-many -t test`
4. **Lint and format**: Use `nx lint project-name` and `nx format project-name`
5. **Build**: Use `nx build project-name` or `nx run-many -t build`

## 🤝 Contributing

1. Create a new branch for your feature
2. Make your changes
3. Run tests and linting: `nx run-many -t test,lint`
4. Commit your changes

## 🎯 Entregables del Challenge

### ✅ **Parte 1 - Prompt Engineering (COMPLETA)**

- **Defensa técnica**: [`notebooks/data-analysis/challenge-genai-20250610.ipynb`](notebooks/data-analysis/challenge-genai-20250610.ipynb)
- **Implementación funcional**: `apps/itti-backend/` (FastAPI + LangChain + OpenAI)
- **Dataset de evaluación**: Integrado en el código
- **Métricas y análisis**: Incluido en notebook y evaluator.py
- **Demo ejecutable**: `test_demo.py`

### 🔄 **Parte 2 - Arquitectura Cognitiva (PENDIENTE)**

- Planificado para `challenge-solutions/part2-cognitive-architecture/`

## 📄 Licencia

Este proyecto es una solución técnica para el challenge de ITTI 2025.

---

📋 **Para revisar la defensa técnica completa, abrir el notebook**: [`notebooks/data-analysis/challenge-genai-20250610.ipynb`](notebooks/data-analysis/challenge-genai-20250610.ipynb)
