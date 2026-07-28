import aiosmtplib

from email.message import EmailMessage

from app.core.config import settings


async def send_email(
    to_email: str,
    subject: str,
    body: str,
):
    message = EmailMessage()

    message["From"] = settings.SMTP_FROM_EMAIL
    message["To"] = to_email
    message["Subject"] = subject

    message.set_content(body)

    await aiosmtplib.send(
        message,
        hostname=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        username=settings.SMTP_USERNAME,
        password=settings.SMTP_PASSWORD,
        start_tls=True,
    )

