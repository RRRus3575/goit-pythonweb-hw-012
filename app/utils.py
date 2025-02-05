import smtplib
from email.mime.text import MIMEText
import os
from aiosmtplib import send

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

if not all([SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD]):
    raise ValueError("❌ SMTP настройки не заданы в .env")

# Функция для отправки письма подтверждения
async def send_verification_email(subject, body, to_email):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = os.getenv("SMTP_USER")
    msg["To"] = to_email

    try:
        await send(
            msg,
            hostname=os.getenv("SMTP_SERVER"),
            port=int(os.getenv("SMTP_PORT")),
            username=os.getenv("SMTP_USER"),
            password=os.getenv("SMTP_PASSWORD"),
            start_tls=True,
        )
        print("✅ Email успешно отправлен!")
    except Exception as e:
        print(f"❌ Ошибка при отправке email: {e}")

# Функция для отправки письма сброса пароля
async def send_reset_email(to_email: str, reset_link: str):
    """
    Asynchronously send a password reset email.

    :param to_email: Recipient email.
    :param reset_link: Password reset link.
    """
    try:
        subject = "Сброс пароля"
        body = f"Для сброса пароля перейдите по ссылке: {reset_link}"

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = os.getenv("SMTP_USER")
        msg["To"] = to_email

        await send(
            msg,
            hostname=os.getenv("SMTP_SERVER"),
            port=int(os.getenv("SMTP_PORT")),
            username=os.getenv("SMTP_USER"),
            password=os.getenv("SMTP_PASSWORD"),
            start_tls=True,
        )

        print("✅ Письмо для сброса пароля успешно отправлено!")
    except Exception as e:
        print(f"❌ Ошибка при отправке email: {e}")
