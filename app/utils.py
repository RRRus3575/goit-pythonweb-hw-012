import smtplib
from email.mime.text import MIMEText
import os

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

if not all([SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD]):
    raise ValueError("❌ SMTP настройки не заданы в .env")

# Функция для отправки письма подтверждения
def send_verification_email(subject, body, to_email):
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = SMTP_USER
        msg["To"] = to_email

        with smtplib.SMTP(SMTP_SERVER, int(SMTP_PORT)) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, to_email, msg.as_string())
        print("✅ Email успешно отправлен!")
    except Exception as e:
        print(f"❌ Ошибка при отправке email: {e}")

# Функция для отправки письма сброса пароля
def send_reset_email(to_email: str, reset_link: str):
    try:
        subject = "Сброс пароля"
        body = f"Для сброса пароля перейдите по ссылке: {reset_link}"
        
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = SMTP_USER
        msg["To"] = to_email

        with smtplib.SMTP(SMTP_SERVER, int(SMTP_PORT)) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, to_email, msg.as_string())

        print("✅ Письмо для сброса пароля успешно отправлено!")
    except Exception as e:
        print(f"❌ Ошибка при отправке email: {e}")
