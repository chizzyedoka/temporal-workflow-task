from datetime import timedelta
from temporalio import workflow


@workflow.defn
class TodoWorkflow:
    @workflow.run
    async def run(self, url: str) -> list:
        todos = await workflow.execute_activity(
            "fetch_todos",  # ← Use string name instead of importing
            url,
            start_to_close_timeout=timedelta(seconds=10),
        )
        return todos