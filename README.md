# 📊 Chat with your CSV

A simple Streamlit app that lets you upload a CSV file and ask questions about it in plain English. It uses [PandasAI](https://github.com/sinaptik-ai/pandas-ai) to turn your questions into pandas code, and [LiteLLM](https://github.com/BerriAI/litellm) to connect PandasAI to an LLM (OpenAI by default, with local Ollama support as an alternative).

## Features

- Upload any CSV and preview it in the browser
- Ask questions about your data in a chat interface
- Keeps full conversation history (previous questions and answers stay visible)
- Answers render properly — tables as tables, charts as images, text as formatted markdown
- Basic input validation on both the uploaded file and the chat messages

## Requirements

- Python **3.11**
- [uv](https://docs.astral.sh/uv/) for dependency management
- An OpenAI API key (or a local [Ollama](https://ollama.com) install if you prefer a local model)

## Setup

1. **Clone or download this project**, then move into its folder:
```bash
   cd csv_chat
```

2. **Pin the Python version** (only needed once):
```bash
   uv python install 3.11
   uv python pin 3.11
```

3. **Install dependencies**:
```bash
   uv add pandasai pandasai-litellm streamlit python-dotenv
```

4. **Set up your API key.** Copy `.env.example` to `.env` and fill in your key:
```bash
   cp .env.example .env
```
