# sys: modifying Python's module search path 
import sys

# import os so we can work with file paths safely
import os

# add parent folder of this file  to Python's import path
# this lets this script import files from folders like db/.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import smtplib
# MIMEText to create a simple text email message
from email.mime.text import MIMEText
# to read emails from Gmail inbox
import imaplib
# to parse raw email messages
import email
# email.utils to convert email dates into timestamps
import email.utils
# Import decode_header to properly read encoded email subject lines
from email.header import decode_header
# Import time to pause the program between inbox checks
import time

# This gets the temperature limit for the selected fridge
from db.database import get_threshold
# import scripts.gpio_controller as gpio_controller


# =========================
# CONFIG
# =========================

# Choose which fridge this script is checking
fridge_name = "fridge1"

# Get the temperature threshold for this fridge from the database
threshold = get_threshold(fridge_name)

# If the database has no threshold saved, use a default value
if threshold is None:
    print("No threshold found, using default 8°C")
    threshold = 8


# =========================
# SEND EMAIL FUNCTION
# =========================
# This function sends an email alert.
def send_email(subject, body, sender, recipients, password):
    # Create a plain text email body
    msg = MIMEText(body)

    # Set the email subject
    msg['Subject'] = subject
    # Set the sender email address.
    msg['From'] = sender
    # Set the recipient list as one readable string
    msg['To'] = ', '.join(recipients)

# Connect securely to Gmail SMTP using SSL on port 465
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        # Log in to Gmail using the sender email and app password
        smtp_server.login(sender, password)
        # Send the email to all recipients
        smtp_server.sendmail(sender, recipients, msg.as_string())

    print("Message sent!")


# =========================
#CHECK REPLY FUNCTION
# =========================

# This function checks the inbox for a new reply containing YES
def check_reply_to_test_subject(username, password, since_time):

    # Connect securely to Gmail IMAP server
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(username, password)
    mail.select('inbox')

# Search all emails in the inbox
    result, data = mail.search(None, 'ALL')
    # Get all email IDs from the search result
    email_ids = data[0].split()

 # Check only the latest 20 emails to keep the program faster
    for e_id in reversed(email_ids[-20:]):  
        # Download the full email content
        result, msg_data = mail.fetch(e_id, '(RFC822)')
        # Get the raw email bytes
        raw_email = msg_data[0][1]
         # Convert the raw email into a readable email object
        msg = email.message_from_bytes(raw_email)

        #  CHECK EMAIL TIME
        date_tuple = email.utils.parsedate_tz(msg['Date'])
        # If the email has a valid date, convert it to a timestamp
        if date_tuple:
            email_timestamp = email.utils.mktime_tz(date_tuple)

            #  Skip old emails
            if email_timestamp < since_time:
                continue

        # SUBJECT
        subject = msg["Subject"]
        # Decode the subject in case it contains special characters
        if subject:
            subject, encoding = decode_header(subject)[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8")

        print("DEBUG SUBJECT:", subject)

# Check if this email is related to the fridge alert
        if subject and "FRIDGE ALERT" in subject.upper():

            # BODY
            body = ""
# If the email has multiple parts, loop through them
            if msg.is_multipart():
                if msg.is_multipart():
                    for part in msg.walk():
                        # Get the content type, such as text/plain or text/html
                        content_type = part.get_content_type()
                        # Get content disposition to detect attachments.
                        content_disposition = str(part.get("Content-Disposition"))

                        #   # Skip attachments because we only want the reply text
                        if "attachment" in content_disposition:
                            continue

                        #  prefer plain text
                        if content_type == "text/plain":
                            body = part.get_payload(decode=True).decode(errors="ignore")
                             # Stop if we found actual text
                            if body.strip():
                                break

                        # fallback to HTML if plain text empty
                        elif content_type == "text/html" and not body:
                            html_body = part.get_payload(decode=True).decode(errors="ignore")
                            body = html_body  
                            # If the email is not multipart, read its body directly
            else:
                 # Print the body for debugging
                body = msg.get_payload(decode=True).decode(errors="ignore")

            print("DEBUG BODY:", repr(body))
 # clean the body by removing spaces and converting to uppercase
            clean_body = body.strip().upper()
            # ff the reply starts with YES, approve turning on the fan.

            if clean_body.startswith("YES"):
                print(" YES DETECTED!")
                mail.logout()
                # Return True to tell the main program that YES was found
                return True
# Log out of the mailbox before returning
    mail.logout()
    return False


# =========================
# MAIN PROGRAM
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
        print(" Checking for reply...")

        if check_reply_to_test_subject(EMAIL, PASSWORD):
            print("TURNING FAN ON...")

            # gpio_controller.spinMotor()
# Keep the fan on for 5 seconds
            time.sleep(5)

            # gpio_controller.stopMotor()
# Stop the loop after the fan action is complete
            break
# Wait 5 seconds before checking the inbox again
        time.sleep(5)