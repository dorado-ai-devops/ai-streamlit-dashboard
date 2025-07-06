# AI Streamlit Dashboard

**Panel interactivo para visualizar y explorar el análisis IA aplicado a DevOps.**

Este proyecto proporciona una interfaz construida con Streamlit para mostrar los prompts, las respuestas de la IA y los metadatos generados por el sistema [`devops-ai-lab`](https://github.com/dorado-ai-devops/devops-ai-lab).

## 🔍 Funcionalidades

- Visualización del análisis generado por IA sobre:
  - Logs de Jenkins
  - Linting de Helm Charts
  - Generación de pipelines
- Filtros y navegación por tipo (`log`, `lint`, `pipeline`, `mcp`)
- Vista detallada con input, prompt, respuesta y resumen simbólico
- Diseño modular: fácil de ampliar con agentes o backend

## 📁 Estructura del proyecto

```
ai-streamlit-dashboard/
├── dashboard.py         # App principal de Streamlit
├── data_loader.py       # Lógica de parsing de JSON / carpetas
├── requirements.txt     # Dependencias: Streamlit, pandas, etc.
├── /mnt/data/gateway/   # Datos de prompt + respuesta del sistema devops-ai-lab
└── /mnt/data/mcp/       # Metadatos de trazabilidad simbólica de devops-ai-lab
```

## 🚀 Cómo empezar

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecutar la app:
```bash
streamlit run dashboard.py
```

3. Asegúrate de que existan las rutas `/mnt/data/gateway/` y `/mnt/data/mcp/` con archivos JSON válidos.

## 🧠 Contexto del proyecto

Este panel forma parte de un sistema modular que combina pipelines DevOps con razonamiento basado en modelos de lenguaje (LLM).  
Para más contexto, consulta el repositorio principal: [`devops-ai-lab`](https://github.com/dorado-ai-devops/devops-ai-lab).

## 📄 Licencia

Licencia MIT.  
Desarrollado como parte de una infraestructura personal DevOps+IA.