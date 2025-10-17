import json
import argparse
from store import get_all_tasks, load_tasks_from_file


def main():
    # Load persisted file if it exists so we can inspect DB across runs
    load_tasks_from_file()
    tasks = get_all_tasks()
    print(f"Total tasks in in-memory DB: {len(tasks)}\n")

    # Pretty print first 10 tasks
    for i, task in enumerate(tasks[:10], start=1):
        print(
            f"{i}. ID {task.get('id')}: {task.get('title')} (Completed: {task.get('completed')})"
        )

    print(
        "\nTo persist or update the dump, re-run the workflow or run this script with --dump."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dump", action="store_true", help="Write full DB to tasks_dump.json"
    )
    args = parser.parse_args()
    main()
    if args.dump:
        with open("tasks_dump.json", "w", encoding="utf-8") as f:
            json.dump(get_all_tasks(), f, indent=2, ensure_ascii=False)
        print("\nWrote full in-memory DB to tasks_dump.json")
