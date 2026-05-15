# Gumshoe — AI Chat Bot

A multi-turn AI chat bot built with the Anthropic API and Claude. Runs as both a CLI tool and a web app.

Built as a learning project to understand the fundamentals of LLM-powered apps: stateless APIs, conversation history, streaming, token tracking, and system prompts.

## Features

- Multi-turn conversation with persistent message history
- Streaming responses
- Token usage tracking per message and across the session
- System prompt persona (a noir detective who loves pizza)
- CLI interface and a minimal web UI via FastAPI

## Project Structure

```
chat.py          # Core chat logic and CLI entry point
app.py           # FastAPI web server
static/
  index.html     # Web UI
requirements.txt
```

## Setup

1. Clone the repo and create a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your Anthropic API key:

```
ANTHROPIC_API_KEY=your_key_here
```

## Usage

**CLI:**

```bash
python chat.py
```

Conversation history is saved to `message-history.json` on exit and reloaded on next run. Type `quit`, `exit`, or `q` to end the session.

**Web UI:**

```bash
uvicorn app:app --reload
```

Open `http://localhost:8000` in your browser.

## Key Concepts

- **Stateless API** — the Anthropic API holds no session state. The full conversation history is sent with every request, which is why token usage grows each turn.
- **System prompt** — set outside the message array; shapes the model's behavior and persona for the entire conversation.
- **Streaming** — responses are printed token by token as they arrive rather than waiting for the full response.
