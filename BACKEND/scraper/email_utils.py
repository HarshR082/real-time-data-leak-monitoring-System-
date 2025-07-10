import smtplib
from email.mime.text import MIMEText

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "your_email@gmail.com"         # <-- Your sender email
EMAIL_PASSWORD = "your_email_app_password"    # <-- Use App Password or real password

def send_alert_email(recipient_email: str, keyword: str, snippet: str, link: str):
    subject = f"Data Sentinel Alert - Keyword Matched: {keyword}"
    body = f"""
Hello,

Your keyword "{keyword}" was found in a new Pastebin post!

Snippet:
{snippet}

Link:
{link}

Stay safe,
Data Sentinel
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = recipient_email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, recipient_email, msg.as_string())
        print(f"[EMAIL] Sent alert email to {recipient_email}")
    except Exception as e:
        print(f"[EMAIL ERROR] Failed to send email: {e}")
import smtplib
from email.mime.text import MIMEText

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "your_email@gmail.com"         # <-- Your sender email
EMAIL_PASSWORD = "your_email_app_password"    # <-- Use App Password or real password

def send_alert_email(recipient_email: str, keyword: str, snippet: str, link: str):
    subject = f"Data Sentinel Alert - Keyword Matched: {keyword}"
    body = f"""
Hello,

Your keyword "{keyword}" was found in a new Pastebin post!

Snippet:
{snippet}

Link:
{link}

Stay safe,
Data Sentinel
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = recipient_email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, recipient_email, msg.as_string())
        print(f"[EMAIL] Sent alert email to {recipient_email}")
    except Exception as e:
        print(f"[EMAIL ERROR] Failed to send email: {e}")
