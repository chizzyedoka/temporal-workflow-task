from typing import Dict, Any
import json
from pathlib import Path

# In-memory database to store tasks, make it exportable
tasksDb: list[Dict[str, Any]] = []


def get_all_tasks():
    return tasksDb


def clear_tasks():
    # Clear the existing list in-place so any external references stay valid.
    tasksDb.clear()

def add_task(task):
    tasksDb.append(task)


def save_tasks_to_file(path: str | Path = "tasks_dump.json") -> None:
    """Persist the in-memory tasks to a JSON file.

    This is a convenience so the in-memory DB can be inspected across
    separate Python processes.
    """
    p = Path(path)
    p.write_text(json.dumps(tasksDb, indent=2, ensure_ascii=False), encoding="utf-8")


def load_tasks_from_file(path: str | Path = "tasks_dump.json") -> None:
    """Load tasks from a JSON file into the in-memory DB (replacing current
    contents).
    """
    p = Path(path)
    if not p.exists():
        return
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(data, list):
            clear_tasks()
            tasksDb.extend(data)
    except Exception:
        # If file corrupt or unreadable, ignore and leave in-memory DB intact.
        pass


__all__ = [
    "tasksDb",
    "get_all_tasks",
    "clear_tasks",
    "add_task",
    "save_tasks_to_file",
    "load_tasks_from_file",
]
