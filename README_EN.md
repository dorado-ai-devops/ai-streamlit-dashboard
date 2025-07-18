# AI Streamlit Dashboard

**Interactive dashboard to visualize and explore AI-assisted DevOps insights.**

This project provides a Streamlit-based user interface to display prompts, AI responses, and metadata generated by the [`devops-ai-lab`](https://github.com/dorado-ai-devops/devops-ai-lab) system.

## 🔍 Features

- View AI-generated analysis from:
  - Jenkins logs
  - Helm chart linting
  - Pipeline generation
- Filter and browse by type (`log`, `lint`, `pipeline`, `mcp`)
- Detailed view: input, prompt, response, and summary
- Modular design: easy to expand with agents or backend enhancements

## 📁 Folder Structure

```
ai-streamlit-dashboard/
├── dashboard.py         # Main Streamlit app
├── data_loader.py       # JSON / directory parsing logic
├── requirements.txt     # Streamlit, pandas, etc.
├── /mnt/data/gateway/   # Prompt + response data from devops-ai-lab
└── /mnt/data/mcp/       # Trace metadata from devops-ai-lab
```

## 🚀 Getting Started

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the app:
```bash
streamlit run dashboard.py
```

3. Make sure `/mnt/data/gateway/` and `/mnt/data/mcp/` exist and contain valid JSON traces.

## 🧠 Project Context

This dashboard is part of a modular system that combines DevOps pipelines with LLM-based reasoning.  
For more context, see the core repo: [`devops-ai-lab`](https://github.com/dorado-ai-devops/devops-ai-lab).

## 📄 License

MIT License.  
Developed as part of a personal DevOps+AI infrastructure.