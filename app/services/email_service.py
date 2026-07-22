"""Transactional email helpers."""
import smtplib
from email.message import EmailMessage

from app.core.config import settings


def send_password_reset_email(full_name: str, recipient: str, reset_url: str) -> None:
    """Send a password-reset link using the configured SMTP account."""
    if not all((settings.SMTP_USERNAME, settings.SMTP_PASSWORD, settings.SMTP_FROM_EMAIL)):
        raise RuntimeError("SMTP credentials are not configured")

    message = EmailMessage()
    message["Subject"] = "Reset your Smart Job Skill Gap Analyzer password"
    message["From"] = settings.SMTP_FROM_EMAIL
    message["To"] = recipient
    message.set_content(
        f"Hello {full_name},\n\n"
        "Use the link below to reset your password. It expires soon.\n\n"
        f"{reset_url}\n"
    )

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=15) as smtp:
        smtp.starttls()
        smtp.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        smtp.send_message(message)
