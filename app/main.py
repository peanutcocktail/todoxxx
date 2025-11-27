from datetime import datetime
from pathlib import Path
import sqlite3
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field


BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "todos.db"
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="Todo App", version="1.0.0")


class Todo(BaseModel):
    id: int
    title: str
    completed: bool
    created_at: str


class TodoCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)


class TodoUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    completed: Optional[bool] = None


def init_db() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            )
            """
        )


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def row_to_todo(row: sqlite3.Row) -> Todo:
    return Todo(
        id=row["id"],
        title=row["title"],
        completed=bool(row["completed"]),
        created_at=row["created_at"],
    )


def fetch_todo(todo_id: int) -> sqlite3.Row:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Todo not found")
    return row


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/", response_class=HTMLResponse)
def read_index() -> HTMLResponse:
    html_path = STATIC_DIR / "index.html"
    if not html_path.exists():
        raise HTTPException(status_code=500, detail="UI missing")
    return HTMLResponse(html_path.read_text(encoding="utf-8"))


@app.get("/api/todos", response_model=List[Todo])
def list_todos() -> List[Todo]:
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM todos ORDER BY created_at DESC, id DESC").fetchall()
    return [row_to_todo(row) for row in rows]


@app.post("/api/todos", response_model=Todo, status_code=201)
def create_todo(payload: TodoCreate) -> Todo:
    title = payload.title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    created_at = datetime.utcnow().isoformat()
    with get_conn() as conn:
        cursor = conn.execute(
            "INSERT INTO todos (title, completed, created_at) VALUES (?, ?, ?)",
            (title, 0, created_at),
        )
        todo_id = cursor.lastrowid
    return row_to_todo(fetch_todo(todo_id))


@app.patch("/api/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, payload: TodoUpdate) -> Todo:
    existing = fetch_todo(todo_id)
    new_title = existing["title"] if payload.title is None else payload.title.strip()
    if new_title == "":
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    new_completed = bool(existing["completed"]) if payload.completed is None else payload.completed
    with get_conn() as conn:
        conn.execute(
            "UPDATE todos SET title = ?, completed = ? WHERE id = ?",
            (new_title, int(new_completed), todo_id),
        )
    return row_to_todo(fetch_todo(todo_id))


@app.delete("/api/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int) -> None:
    # Ensure the todo exists before attempting deletion
    fetch_todo(todo_id)
    with get_conn() as conn:
        conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
