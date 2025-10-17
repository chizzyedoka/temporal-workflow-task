# workflows.py

from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy  


@workflow.defn
class TodoWorkflow:
    @workflow.run
    async def run(self, url: str) -> list:

        # 2. Define your retry policy
        fetch_retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=1),  # Wait 1s after first failure
            backoff_coefficient=2.0,              # Double the wait time for each retry
            maximum_attempts=3,                   # Try a total of 3 times
        )

        # Step 1: Fetch todos
        workflow.logger.info("Starting activity: fetch_todos")
        todos = await workflow.execute_activity(
            "fetch_todos",
            url,
            start_to_close_timeout=timedelta(seconds=10),
            retry_policy=fetch_retry_policy,  
        )
        workflow.logger.info("Activity fetch_todos completed")

        # Step 2: Transform todos
        workflow.logger.info("Starting activity: transform_todos")
        transformed_todos = await workflow.execute_activity(
            "transform_todos",
            todos,
            start_to_close_timeout=timedelta(seconds=10),
        )
        workflow.logger.info("Activity transform_todos completed")

        return transformed_todos