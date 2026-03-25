

# =========================
# 📚 IMPORTS
# =========================
import smtplib
from email.mime.text import MIMEText
import imaplib
import email
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
def check_reply_to_test_subject(username, password):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(username, password)
    mail.select('inbox')

    result, data = mail.search(None, 'ALL')
    email_ids = data[0].split()

    # check latest 10 emails
    for e_id in reversed(email_ids[-10:]):
        result, msg_data = mail.fetch(e_id, '(RFC822)')
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject = msg["Subject"]

        # decode subject
        if subject:
            subject, encoding = decode_header(subject)[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8")

        # ONLY CHECK REPLIES
        if subject and "Re: Test Subject" in subject:

            body = ""

            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode(errors="ignore")
                        break
            else:
                body = msg.get_payload(decode=True).decode(errors="ignore")

            print("📩 Found reply!")
            print("Body:", body)

            first_line = body.strip().splitlines()[0]

            if first_line.upper() == "YES":
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