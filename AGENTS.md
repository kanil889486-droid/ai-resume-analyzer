# AI Agent Instructions

## Project overview
This is a small Python Flask web application for an AI resume analyzer.
- Main application: `app.py`
- Templates are embedded in `app.py` and no separate build system exists.
- Dependencies are listed in `requirements.txt`.

## Build / install command
There is no compiled build step. To prepare the environment:

```bash
python -m pip install -r requirements.txt
```

## Run commands
For local development:

```bash
python app.py
```

For production-style hosting using Gunicorn:

```bash
gunicorn app:app
```

## Notes for agents
- Do not assume a frontend build tool is present; this is a server-rendered Flask app.
- There are no automated tests in the repository.
- If asked to improve functionality, update `app.py` and keep HTML/CSS simple.
