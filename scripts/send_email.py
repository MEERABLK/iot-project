# =========================
# 📦 FIX IMPORT PATH
# =========================
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# =========================
# 📚 IMPORTS
# =========================
import smtplib
from email.mime.text import MIMEText
import imaplib
import email
import email.utils
from email.header import decode_header
import time

from db.database import get_threshold
import scripts.gpio_controller as gpio_controller


# =========================
# ⚙️ CONFIG
# =========================
fridge_name = "fridge1"

threshold = get_threshold(fridge_name)


if threshold is None:
    print("No threshold found, using default 8°C")
    threshold = 8


# =========================
# 📧 SEND EMAIL FUNCTION
# =========================
def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)

    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())

    print("✅ Message sent!")


# =========================
# 📩 CHECK REPLY FUNCTION
# =========================
def check_reply_to_test_subject(username, password, since_time):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(username, password)
    mail.select('inbox')

    result, data = mail.search(None, 'ALL')
    email_ids = data[0].split()

    for e_id in reversed(email_ids[-20:]):  # last 20 emails only
        result, msg_data = mail.fetch(e_id, '(RFC822)')
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        # ✅ CHECK EMAIL TIME
        date_tuple = email.utils.parsedate_tz(msg['Date'])
        if date_tuple:
            email_timestamp = email.utils.mktime_tz(date_tuple)

            # ❌ Skip old emails
            if email_timestamp < since_time:
                continue

        # SUBJECT
        subject = msg["Subject"]
        if subject:
            subject, encoding = decode_header(subject)[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8")

        print("DEBUG SUBJECT:", subject)

        if subject and "FRIDGE ALERT" in subject.upper():

            # BODY
            body = ""

            if msg.is_multipart():
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))

                        # ✅ skip attachments
                        if "attachment" in content_disposition:
                            continue

                        # ✅ prefer plain text
                        if content_type == "text/plain":
                            body = part.get_payload(decode=True).decode(errors="ignore")
                            if body.strip():
                                break

                        # ✅ fallback to HTML if plain text empty
                        elif content_type == "text/html" and not body:
                            html_body = part.get_payload(decode=True).decode(errors="ignore")
                            body = html_body  # temporary fallback
            else:
                body = msg.get_payload(decode=True).decode(errors="ignore")

            print("DEBUG BODY:", repr(body))

            clean_body = body.strip().upper()

            if clean_body.startswith("YES"):
                print("✅ YES DETECTED!")
                mail.logout()
                return True

    mail.logout()
    return False


# =========================
# 🚀 MAIN PROGRAM
# =========================
if __name__ == "__main__":
    EMAIL = "your_email@gmail.com"
    PASSWORD = "your_app_password"

    # SEND TEST EMAIL
    send_email(
        subject="Test Subject",
        body="Reply YES to turn on the fan",
        sender=EMAIL,
        recipients=[EMAIL],
        password=PASSWORD
    )

    # WAIT FOR REPLY
    while True:
        print("⏳ Checking for reply...")

        if check_reply_to_test_subject(EMAIL, PASSWORD):
            print("🔥 TURNING FAN ON...")

            gpio_controller.spinMotor()

            time.sleep(5)

            gpio_controller.stopMotor()

            break

        time.sleep(5)