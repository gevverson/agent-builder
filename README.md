# Agent Builder

A small Flask app for creating custom AI chat agents. Each agent has its own instructions; every conversation is stored per agent and sent back to Google Gemini as context, so an agent remembers earlier turns.

> Early prototype (2025). It has no user accounts, so run it locally or behind your own access control.

## Features

- **Admin page** to create and delete agents (name + instructions)
- **Chat page per agent**, backed by a JSON endpoint (`POST /chat/<agent_id>`)
- **Conversation memory** stored in SQLite through Flask-SQLAlchemy (`Agent` → `Conversation`, cascade delete)
- **Gemini** responses through the `google-genai` SDK
- **CI/CD** with GitHub Actions: install, smoke-test the app factory, then call a webhook that pulls and reloads the PythonAnywhere deployment

## Stack

Python · Flask (app factory + blueprint) · Flask-SQLAlchemy · SQLite · Google Gemini · GitHub Actions · PythonAnywhere

## Run locally

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "GEMINI_API_KEY=your-key" > .env
python run.py
```

Then open http://127.0.0.1:5000.

## Layout

```
app/
  __init__.py     # create_app() factory
  routes.py       # admin, chat page, chat API, delete, deploy webhook
  models.py       # Agent, Conversation
  gemini.py       # prompt building + Gemini call + saving history
  templates/      # admin.html, chat.html
config.py         # reads GEMINI_API_KEY from .env
run.py
```
