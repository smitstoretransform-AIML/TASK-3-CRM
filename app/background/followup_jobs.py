import asyncio
from datetime import date, datetime, timezone

from app.core.database import SessionLocal
from app.core.email import send_email
from app.models.customers import Customer
from app.models.follow_ups import FollowUp
from app.models.notifications import Notification
from app.models.users import User


def process_followup_reminders():
    db = SessionLocal()

    try:
        today = date.today()

        followups = (
            db.query(
                FollowUp,
                Customer,
                User
            )
            .join(
                Customer,
                FollowUp.customer_id == Customer.id
            )
            .join(
                User,
                Customer.created_by == User.id
            )
            .filter(
                FollowUp.status == "pending",
                FollowUp.date <= today,
                FollowUp.reminder_sent_at.is_(None),
                Customer.deleted_at.is_(None)
            )
            .all()
        )

        notifications_created = 0
        emails_sent = 0

        for followup, customer, user in followups:

            print(
                "Processing follow-up: "
                f"FollowUp ID={followup.id}, "
                f"Customer ID={customer.id}, "
                f"Customer={customer.name}, "
                f"User ID={user.id}, "
                f"User Email={user.email}"
            )

            notification_message = (
                f"You have a {followup.type} "
                f"follow-up for customer "
                f"{customer.name}."
            )

            # -------------------------------------------------
            # 1. Create In-App Notification
            # -------------------------------------------------

            notification = Notification(
                user_id=user.id,
                title="Follow-up Reminder",
                message=notification_message,
                is_read=False
            )

            db.add(notification)

            # Force SQLAlchemy to execute the INSERT
            # and generate the notification ID.
            db.flush()

            notifications_created += 1

            print(
                "Notification created successfully: "
                f"Notification ID={notification.id}, "
                f"User ID={notification.user_id}"
            )

            # -------------------------------------------------
            # 2. Send Email Notification
            # -------------------------------------------------

            try:
                asyncio.run(
                    send_email(
                        to_email=user.email,
                        subject="CRM Follow-up Reminder",
                        body=(
                            f"Hello {user.name},\n\n"
                            f"You have a {followup.type} "
                            f"follow-up scheduled for customer "
                            f"{customer.name}.\n\n"
                            f"Follow-up Date: "
                            f"{followup.date}\n"
                            f"Notes: "
                            f"{followup.notes or 'No notes provided'}\n\n"
                            f"Please review this follow-up "
                            f"in your CRM system.\n\n"
                            f"Regards,\n"
                            f"CRM Task 3"
                        )
                    )
                )

                emails_sent += 1

                print(
                    "Email sent successfully to "
                    f"{user.email}"
                )

            except Exception as email_error:

                print(
                    "Failed to send email to "
                    f"{user.email}: "
                    f"{email_error}"
                )

            # -------------------------------------------------
            # 3. Mark Reminder as Processed
            # -------------------------------------------------

            followup.reminder_sent_at = datetime.now(
                timezone.utc
            )

        # -----------------------------------------------------
        # 4. Save Database Changes
        # -----------------------------------------------------

        db.commit()

        print(
            "Follow-up reminder job completed successfully. "
            f"Notifications created: "
            f"{notifications_created}, "
            f"Emails sent: "
            f"{emails_sent}"
        )

    except Exception as e:

        db.rollback()

        print(
            "Error processing follow-up reminders: "
            f"{e}"
        )

    finally:

        db.close()

