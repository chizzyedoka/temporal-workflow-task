import asyncio
import logging  
import os
from temporalio.client import Client
from temporalio.worker import Worker
from temporalio.runtime import PrometheusConfig, Runtime, TelemetryConfig
from workflows import TodoWorkflow
from activities import fetch_todos, transform_todos


async def main():
    logging.basicConfig(level=logging.INFO)
    # Get Temporal server address from an environment variable or use default
    temporal_server_address = os.getenv("TEMPORAL_SERVER_ADDRESS", "localhost:7233")
    # define the prometheus metrics endpoint
    metrics_config = PrometheusConfig(bind_address="0.0.0.0:9090")
    runtime = Runtime(telemetry=TelemetryConfig(metrics=metrics_config))
    client = await Client.connect(temporal_server_address, runtime=runtime)

    async with Worker(
        client,
        task_queue="todo-task-queue",
        workflows=[TodoWorkflow],
        activities=[fetch_todos, transform_todos],
    ):
        # We use logger.info instead of print for consistency
        logging.info("Worker started; listening for tasks...")
        logging.info("Prometheus metrics available at http://localhost:9090/metrics")
        await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())