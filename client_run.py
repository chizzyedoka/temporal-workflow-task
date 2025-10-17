import asyncio
from temporalio.client import Client
from workflows import TodoWorkflow
from store import get_all_tasks, clear_tasks, add_task, save_tasks_to_file


async def main():
    client = await Client.connect("localhost:7233")

    # Execute workflow and get the result
    result = await client.execute_workflow(
        TodoWorkflow.run,
        "https://jsonplaceholder.typicode.com/todos",
        id="todo-workflow-3",
        task_queue="todo-task-queue",
    )

    print("\n Workflow completed successfully!")

    # Save the returned tasks to the client's database using store API
    clear_tasks()
    for task in result:
        add_task(task)

    # Persist to disk so other processes (or a later run) can inspect the DB
    save_tasks_to_file()

    # Now check the database
    saved_tasks = get_all_tasks()
    print(f"\n Total tasks saved in database: {len(saved_tasks)}")
    print("\nFirst 5 tasks from database:")
    for task in saved_tasks[:5]:
        print(f"  - ID {task['id']}: {task['title']} (Completed: {task['completed']})")


if __name__ == "__main__":
    asyncio.run(main())
