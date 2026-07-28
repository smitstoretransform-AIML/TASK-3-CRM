from apscheduler.schedulers.background import BackgroundScheduler

from app.background.followup_jobs import (
    process_followup_reminders
)

from app.reports.daily_crm_report import (
    generate_daily_crm_report
)


scheduler = BackgroundScheduler()


def start_scheduler():

   # ===========  FOLLOW-UP REMINDERS EVERY 1 MINUTE ==========

    scheduler.add_job(
        process_followup_reminders,
        "interval",
        minutes=1,
        id="followup_reminder_job",
        replace_existing=True,
    )

    # =========== DAILY CRM EVERY 1 MINUTE ==========

    scheduler.add_job(
        generate_daily_crm_report,
        "interval",
        minutes=1,
        id="daily_crm_report_job",
        replace_existing=True,
    )

    # =====================================================
    # PRODUCTION SCHEDULE
    # =====================================================
    # After testing, replace the two interval jobs above
    # with the cron schedules below.
    #
    # Follow-up reminders at 9:00 AM
    #
    # scheduler.add_job(
    #     process_followup_reminders,
    #     "cron",
    #     hour=9,
    #     minute=0,
    #     id="followup_reminder_job",
    #     replace_existing=True,
    # )
    #
    # Daily CRM report at 9:05 AM
    #
    # scheduler.add_job(
    #     generate_daily_crm_report,
    #     "cron",
    #     hour=9,
    #     minute=5,
    #     id="daily_crm_report_job",
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

