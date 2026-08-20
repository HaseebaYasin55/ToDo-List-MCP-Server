"""
storage.py
----------
This file handles everything related to saving and loading todos
from a local JSON file. Keeping this logic in its own file (separate
from server.py) makes the project easier to read and easier to test.

Beginner note:
A JSON file is just a plain text file that stores data in a format
that looks like a Python dictionary/list. We use it here instead of
a real database because it is simple and needs no extra setup.
"""

import json
import os
from datetime import datetime, timezone
from typing import Any

# This is the file where all todos will be saved.
# It will be created automatically the first time you add a todo.
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "todos.json")


def _ensure_data_file_exists() -> None:
    """Create the JSON file with an empty structure if it does not exist yet."""
    if not os.path.exists(DATA_FILE):
        initial_data = {"next_id": 1, "todos": []}
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(initial_data, f, indent=2)


def load_data() -> dict[str, Any]:
    """Read the JSON file from disk and return it as a Python dictionary."""
    _ensure_data_file_exists()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data: dict[str, Any]) -> None:
    """Write the given Python dictionary back to the JSON file on disk."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def add_todo(title: str, description: str = "") -> dict[str, Any]:
    """Add a new todo and save it. Returns the newly created todo."""
    data = load_data()

    new_todo = {
        "id": data["next_id"],
        "title": title,
        "description": description,
        "completed": False,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    data["todos"].append(new_todo)
    data["next_id"] += 1
    save_data(data)

    return new_todo


def get_all_todos() -> list[dict[str, Any]]:
    """Return a list of every todo currently saved."""
    data = load_data()
    return data["todos"]


def get_todo_by_id(todo_id: int) -> dict[str, Any] | None:
    """Return a single todo that matches the given ID, or None if not found."""
    data = load_data()
    for todo in data["todos"]:
        if todo["id"] == todo_id:
            return todo
    return None


def mark_todo_completed(todo_id: int) -> dict[str, Any] | None:
    """Mark a todo as completed. Returns the updated todo, or None if not found."""
    data = load_data()
    for todo in data["todos"]:
        if todo["id"] == todo_id:
            todo["completed"] = True
            save_data(data)
            return todo
    return None


def delete_todo(todo_id: int) -> bool:
    """Delete a todo by ID. Returns True if something was deleted, False otherwise."""
    data = load_data()
    original_length = len(data["todos"])
    data["todos"] = [todo for todo in data["todos"] if todo["id"] != todo_id]

    if len(data["todos"]) == original_length:
        return False  # nothing was removed, so the ID did not exist

    save_data(data)
    return True
