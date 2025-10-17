import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

from workflows import TodoWorkflow
from activities import fetch_todos, transform_todos


async def main():
    client = await Client.connect("localhost:7233")

    async with Worker(
        client,
        task_queue="todo-task-queue",
        workflows=[TodoWorkflow],
        activities=[fetch_todos, transform_todos],  # Added transform_todos
    ):
        print("Worker started; listening for tasks...")
        await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())