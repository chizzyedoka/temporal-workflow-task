# temporal-workflow-task

This example shows a Temporal workflow (`workflows.TodoWorkflow`) that uses an activity (`activities.fetch_todos`) to fetch todos from jsonplaceholder.typicode.com. Blocking HTTP is done in the activity (runs in the worker) while the workflow performs pure computation.

Quick steps:

1. Start Temporal server (quickstart docker):

```powershell
docker run --network=host -d --name temporal2 \ 
  -e TEMPORAL_CLI_ADDRESS=localhost:7233 \ 
  temporalio/auto-setup:latest
```

2. Install deps:

```powershell
python -m pip install -r requirements.txt
```

3. Start the worker:

```powershell
python worker.py
```

4. In a separate shell start the client to run the workflow:

```powershell
python client_run.py
```
