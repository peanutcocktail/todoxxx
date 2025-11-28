# Todo App

A focused, local-first todo tracker with a FastAPI backend and a clean web UI. Tasks are stored in a lightweight SQLite database under `app/data/todos.db`.

## Quick start (Pinokio)

1. **Install** - open `install.js` from the sidebar (default when not installed). This sets up a Python virtual environment and installs the app dependencies with `uv`.
2. **Start** - select `start.js`. Once the server logs a URL, Pinokio will surface an **Open Web UI** link automatically.
3. **Use the app** - add, check off, and delete tasks directly in the UI at the captured URL.
4. **Update or Reset** - `update.js` refreshes Python dependencies; `reset.js` removes the virtualenv and local database if you want a clean slate.

## Project layout

- `app/main.py` - FastAPI server, SQLite storage, and API routes.
- `app/static/index.html` - single-page UI for managing todos.
- `app/requirements.txt` - Python dependencies.
- `install.js` / `start.js` / `update.js` / `reset.js` - Pinokio scripts for lifecycle actions.
- `pinokio.js` / `pinokio.json` - launcher UI and metadata.

## API

Base URL: the same origin as the running app (Pinokio will expose it as `http://<host>:<port>`).

### Endpoints

- `GET /api/todos` -> list todos.
- `POST /api/todos` -> create a todo. Body: `{"title": "string"}`.
- `PATCH /api/todos/{id}` -> update a todo. Body (any field): `{"title": "string", "completed": true}`.
- `DELETE /api/todos/{id}` -> remove a todo.

### Examples

**JavaScript (browser or Node)**

```js
const base = "http://localhost:8000"; // replace with the captured URL

async function addTodo(title) {
  const res = await fetch(`${base}/api/todos`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title })
  });
  return res.json();
}
```

**Python**

```python
import requests

base = "http://localhost:8000"  # replace with the captured URL
resp = requests.post(f"{base}/api/todos", json={"title": "Write docs"})
resp.raise_for_status()
print(resp.json())
```

**cURL**

```bash
curl -X POST "http://localhost:8000/api/todos" \
  -H "Content-Type: application/json" \
  -d '{"title":"Ship the todo app"}'
```

## Notes

- The server binds to `127.0.0.1` with an auto-selected port to avoid conflicts.
- Data persists locally in `app/data/todos.db`. Delete via `reset.js` if you need a fresh start.
