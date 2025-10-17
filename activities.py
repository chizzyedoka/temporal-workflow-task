import requests
from typing import List, Dict, Any
from store import tasksDb
from temporalio import activity


@activity.defn
async def fetch_todos(
    url: str = "https://jsonplaceholder.typicode.com/todos",
) -> List[Dict[str, Any]]:
    response = requests.get(url)
    response.raise_for_status()
    todos = response.json()

    # Persist into in-memory tasks DB (clear previous contents and extend)
    tasksDb.clear()
    if isinstance(todos, list):
        tasksDb.extend(todos)

    return todos


@activity.defn
async def transform_todos(todos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Normalize todos and ensure todo with id==2 is marked completed."""
    for todo in todos:
        # Use get to avoid KeyError on malformed items
        if todo.get("id") == 2:
            todo["completed"] = True
    return todos


__all__ = ["fetch_todos", "transform_todos"]
