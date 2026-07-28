import json
from datetime import date, datetime, time, timezone
from pathlib import Path

from sqlalchemy import func

from app.core.database import SessionLocal
from app.models.customers import Customer
from app.models.follow_ups import FollowUp
from app.models.leads import Lead
from app.models.notifications import Notification


# ---------------------------------------------------------
# Report Storage Directory
# ---------------------------------------------------------

REPORTS_DIR = Path("reports")

REPORTS_DIR.mkdir(
    exist_ok=True
)


def generate_daily_crm_report():
    db = SessionLocal()

    try:
        today = date.today()

        # -------------------------------------------------
        # Today's Date Range
        # -------------------------------------------------

        start_of_day = datetime.combine(
            today,
            time.min
        ).replace(
            tzinfo=timezone.utc
        )

        end_of_day = datetime.combine(
            today,
            time.max
        ).replace(
            tzinfo=timezone.utc
        )

        # -------------------------------------------------
        # Customer Statistics
        # -------------------------------------------------

        total_customers = (
            db.query(
                func.count(Customer.id)
            )
            .filter(
                Customer.deleted_at.is_(None)
            )
            .scalar()
        )

        new_customers_today = (
            db.query(
                func.count(Customer.id)
            )
            .filter(
                Customer.created_at >= start_of_day,
                Customer.created_at <= end_of_day,
                Customer.deleted_at.is_(None)
            )
            .scalar()
        )

        # -------------------------------------------------
        # Lead Statistics
        # -------------------------------------------------

        total_leads = (
            db.query(
                func.count(Lead.id)
            )
            .filter(
                Lead.deleted_at.is_(None)
            )
            .scalar()
        )

        new_leads_today = (
            db.query(
                func.count(Lead.id)
            )
            .filter(
                Lead.created_at >= start_of_day,
                Lead.created_at <= end_of_day,
                Lead.deleted_at.is_(None)
            )
            .scalar()
        )

        # -------------------------------------------------
        # Follow-up Statistics
        # -------------------------------------------------

        total_followups = (
            db.query(
                func.count(FollowUp.id)
            )
            .scalar()
        )

        pending_followups = (
            db.query(
                func.count(FollowUp.id)
            )
            .filter(
                FollowUp.status == "pending"
            )
            .scalar()
        )

        completed_followups = (
            db.query(
                func.count(FollowUp.id)
            )
            .filter(
                FollowUp.status == "completed"
            )
            .scalar()
        )

        overdue_followups = (
            db.query(
                func.count(FollowUp.id)
            )
            .filter(
                FollowUp.status == "pending",
                FollowUp.date < today
            )
            .scalar()
        )

        # -------------------------------------------------
        # Notification Statistics
        # -------------------------------------------------

        notifications_today = (
            db.query(
                func.count(Notification.id)
            )
            .filter(
                Notification.created_at >= start_of_day,
                Notification.created_at <= end_of_day
            )
            .scalar()
        )

        # -------------------------------------------------
        # Build Report
        # -------------------------------------------------

        report = {
            "report_date": today.isoformat(),

            "generated_at": datetime.now(
                timezone.utc
            ).isoformat(),

            "customers": {
                "total": total_customers or 0,
                "new_today": new_customers_today or 0,
            },

            "leads": {
                "total": total_leads or 0,
                "new_today": new_leads_today or 0,
            },

            "followups": {
                "total": total_followups or 0,
                "pending": pending_followups or 0,
                "completed": completed_followups or 0,
                "overdue": overdue_followups or 0,
            },

            "notifications": {
                "created_today": notifications_today or 0,
            },
        }

        # -------------------------------------------------
        # Save Report as JSON
        # -------------------------------------------------

        report_filename = (
            f"daily_crm_report_"
            f"{today.isoformat()}.json"
        )

        report_path = (
            REPORTS_DIR /
            report_filename
        )

        with open(
            report_path,
            "w",
            encoding="utf-8"
        ) as report_file:

            json.dump(
                report,
                report_file,
                indent=4
            )

        # -------------------------------------------------
        # Print Report
        # -------------------------------------------------

        print(
            "\n========== DAILY CRM REPORT =========="
        )

        print(
            f"Report Date: "
            f"{report['report_date']}"
        )

        print(
            f"Generated At: "
            f"{report['generated_at']}"
        )

        print(
            "\nCustomers:"
        )

        print(
            f"  Total: "
            f"{report['customers']['total']}"
        )

        print(
            f"  New Today: "
            f"{report['customers']['new_today']}"
        )

        print(
            "\nLeads:"
        )

        print(
            f"  Total: "
            f"{report['leads']['total']}"
        )

        print(
            f"  New Today: "
            f"{report['leads']['new_today']}"
        )

        print(
            "\nFollow-ups:"
        )

        print(
            f"  Total: "
            f"{report['followups']['total']}"
        )

        print(
            f"  Pending: "
            f"{report['followups']['pending']}"
        )

        print(
            f"  Completed: "
            f"{report['followups']['completed']}"
        )

        print(
            f"  Overdue: "
            f"{report['followups']['overdue']}"
        )

        print(
            "\nNotifications:"
        )

        print(
            f"  Created Today: "
            f"{report['notifications']['created_today']}"
        )

        print(
            "\nReport saved successfully:"
        )

        print(
            f"  {report_path.resolve()}"
        )

        print(
            "======================================\n"
        )

        return report

    except Exception as e:

        print(
            "Error generating daily CRM report: "
            f"{e}"
        )

        return None

    finally:

        db.close()

