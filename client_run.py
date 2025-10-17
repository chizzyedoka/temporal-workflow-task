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
        id="todo-workflow-4",  # Changed ID for new run
        task_queue="todo-task-queue",
    )

    print("\n✅ Workflow completed successfully!")

    # Save the returned tasks to the client's database using store API
    clear_tasks()
    for task in result:
        add_task(task)

    # Persist to disk so other processes (or a later run) can inspect the DB
    save_tasks_to_file()

    # Now check the database
    saved_tasks = get_all_tasks()
    print(f"\n Total tasks saved in database: {len(saved_tasks)}")
    
    # Show tasks for userId 2 to verify transformation
    user2_tasks = [task for task in saved_tasks if task.get("userId") == 2]
    completed_user2 = [task for task in user2_tasks if task.get("completed")]
    print(f"\n Tasks for userId 2: {len(user2_tasks)} total, {len(completed_user2)} completed")
    
    print("\nFirst 5 tasks from database:")
    for task in saved_tasks[:5]:
        print(f"  - ID {task['id']}: {task['title']} (Completed: {task['completed']}, User: {task['userId']})")
    
    print("\nSample tasks from userId 2:")
    for task in user2_tasks[:3]:
        print(f"  - ID {task['id']}: {task['title']} (Completed: {task['completed']})")


if __name__ == "__main__":
    asyncio.run(main())