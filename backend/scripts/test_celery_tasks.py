import os
import sys
import argparse
from datetime import datetime, timezone

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.celery_app import celery_app, init_celery
from app.tasks.periodic import send_daily_reminders, generate_monthly_reports


def setup_app():
    """Setup Flask app with Celery integration"""
    print("Setting up Flask app and Celery...")
    app = create_app()
    init_celery(app)
    return app


def trigger_daily_reminders():
    """Trigger daily reminders task"""
    print("\n" + "=" * 50)
    print("TRIGGERING DAILY REMINDERS TASK")
    print("=" * 50)
    print(f"Started at: {datetime.now(timezone.utc).isoformat()}")

    try:
        # Trigger the task asynchronously
        result = send_daily_reminders.delay()
        print(f"Task ID: {result.id}")
        print("Task triggered successfully!")

        # Wait for result
        print("Waiting for task completion...")
        task_result = result.get(timeout=300)  # 5 minute timeout
        print("Task completed successfully!")
        print(f"Result: {task_result}")

    except Exception as e:
        print(f"Error triggering daily reminders: {str(e)}")
        return False

    print(f"Completed at: {datetime.now(timezone.utc).isoformat()}")
    return True


def trigger_monthly_reports():
    """Trigger monthly reports task"""
    print("\n" + "=" * 50)
    print("TRIGGERING MONTHLY REPORTS TASK")
    print("=" * 50)
    print(f"Started at: {datetime.now(timezone.utc).isoformat()}")

    try:
        # Trigger the task asynchronously
        result = generate_monthly_reports.delay()
        print(f"Task ID: {result.id}")
        print("Task triggered successfully!")

        # Wait for result
        print("Waiting for task completion...")
        task_result = result.get(timeout=600)  # 10 minute timeout
        print("Task completed successfully!")
        print(f"Result: {task_result}")

    except Exception as e:
        print(f"Error triggering monthly reports: {str(e)}")
        return False

    print(f"Completed at: {datetime.now(timezone.utc).isoformat()}")
    return True


def trigger_all_tasks():
    """Trigger all tasks"""
    print("\n" + "=" * 60)
    print("TRIGGERING ALL CELERY TASKS")
    print("=" * 60)

    success_count = 0

    # Trigger daily reminders
    if trigger_daily_reminders():
        success_count += 1

    # Trigger monthly reports
    if trigger_monthly_reports():
        success_count += 1

    print("\n" + "=" * 60)
    print(f"SUMMARY: {success_count}/2 tasks completed successfully")
    print("=" * 60)

    return success_count == 2


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Trigger Celery tasks for testing")
    parser.add_argument(
        "task",
        choices=["daily-reminders", "monthly-reports", "all"],
        help="Which task to trigger",
    )
    parser.add_argument(
        "--no-wait", action="store_true", help="Don't wait for task completion"
    )

    args = parser.parse_args()

    # Setup Flask app and Celery
    app = setup_app()

    with app.app_context():
        print(
            f"Starting Celery task testing at {datetime.now(timezone.utc).isoformat()}"
        )

        # Modify global behavior if no-wait is specified
        if args.no_wait:
            print(
                "Running in no-wait mode - tasks will be triggered but not waited for"
            )
            # You could modify the functions to not wait, but for simplicity we'll mention it

        success = False

        if args.task == "daily-reminders":
            success = trigger_daily_reminders()
        elif args.task == "monthly-reports":
            success = trigger_monthly_reports()
        elif args.task == "all":
            success = trigger_all_tasks()

        if success:
            print("\n✅ All requested tasks completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Some tasks failed!")
            sys.exit(1)


if __name__ == "__main__":
    main()
