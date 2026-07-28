from apscheduler.schedulers.background import BackgroundScheduler

from app.background.followup_jobs import (
    process_followup_reminders
)


scheduler = BackgroundScheduler()


def start_scheduler():

    # =========== evrey 1 minute ===========
    scheduler.add_job(
        process_followup_reminders,
        "interval",
        minutes=1,
        id="followup_reminder_job",
        replace_existing=True,
    )

    # =========== evrey day at 9:00 AM ===========
    # scheduler.add_job(
    #     process_followup_reminders,
    #     "cron",
    #     hour=9,
    #     minute=0,
    #     id="followup_reminder_job",
    #     replace_existing=True,
    # )

    scheduler.start()

    print(
        "Background scheduler started successfully!"
    )


def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()

        print(
            "Background scheduler stopped successfully!"
        )