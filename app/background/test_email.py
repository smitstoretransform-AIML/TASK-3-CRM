import asyncio

from app.core.email import send_email


async def main():
    await send_email(
        to_email="your_test_email@gmail.com",
        subject="CRM Task 3 Email Test",
        body=(
            "This is a test email "
            "from CRM Task 3."
        ),
    )

    print(
        "Test email sent successfully!"
    )


if __name__ == "__main__":
    asyncio.run(main())