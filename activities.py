# activities.py

import requests
from typing import List, Dict, Any
from store import tasksDb
from temporalio import activity


@activity.defn
async def fetch_todos(
    url: str = "https://jsonplaceholder.typicode.com/todos",
) -> List[Dict[str, Any]]:

    attempt = activity.info().attempt
    activity.logger.info(f"Executing fetch_todos, attempt {attempt}")

    if attempt == 1:
        activity.logger.warning("Simulating API failure on attempt 1...")
        # Raising an exception tells Temporal the activity failed
        raise RuntimeError("Simulated API failure")
    # --- End of simulation ---

    activity.logger.info("Attempt 2 (or later) successful. Fetching data...")
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
    """Mark all todos with userId == 2 as completed."""
    activity.logger.info(f"Transforming {len(todos)} todos")
    
    modified_count = 0
    for todo in todos:
        if todo.get("userId") == 2:
            todo["completed"] = True
            modified_count += 1
    
    activity.logger.info(f"Modified {modified_count} todos for userId 2")
    return todos


__all__ = ["fetch_todos", "transform_todos"]