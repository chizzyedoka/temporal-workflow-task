from datetime import timedelta
from temporalio import workflow


@workflow.defn
class TodoWorkflow:
    @workflow.run
    async def run(self, url: str) -> list:
        # Step 1: Fetch todos
        todos = await workflow.execute_activity(
            "fetch_todos",
            url,
            start_to_close_timeout=timedelta(seconds=10),
        )
        
        # Step 2: Transform todos (mark userId 2 as completed)
        transformed_todos = await workflow.execute_activity(
            "transform_todos",
            todos,
            start_to_close_timeout=timedelta(seconds=10),
        )
        
        return transformed_todos