import smtplib
from email.mime.text import MIMEText
import imaplib
import email
from email.header import decode_header 

#Step #1 import smtp library to send email, MIMEText to format the message format, 
# IMAP to read email, email for parsing raw email data, decode_header to decode encoded emails
#like ?UTF-8... 

"""
 ==== Send email ====
create the send email method that takes ubject, body, sender, recipients, password as header parameters
"""
def send_email(subject, body, sender, recipients, password):
  
   #Step #2 create email object
    msg = MIMEText(body)
   
   #Step #3 add email headers
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)

   #Step #3 secure connection with SSL encryption, 465 is the port, server is smtp.gmail.com 
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
   
        #Step #4 login 
        smtp_server.login(sender, password)
      
        #Step #5 send email as string
        smtp_server.sendmail(sender, recipients, msg.as_string())
        print("Message sent!")

#Step #6 call the method: the password is an app password that can be generated from here https://myaccount.google.com/apppasswords
send_email("Test Subject", "This is the body of the email", "lowkeymischievous@gmail.com", ["lowkeymischievous@gmail.com"], "ibrx juqy lako brbr")


"""
==== Read Email needs only username password no recipient ====
"""

def read_email(username, password):
    print("Connecting to Gmail...\n")

    #Step #1 get gmail securely with ssl 
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    
    #Step #2 login
    mail.login(username, password)

    #Step #3 select inbox
    mail.select('inbox')

    #Step #4 search emails get all email ids
    result, data = mail.search(None, 'ALL')
   
    #starting from the first email
    email_ids = data[0].split()


    print(f"Total emails found: {len(email_ids)}\n")
    print("Showing last 5 emails:\n")

    count = 1

    #Step #5 get first 5 emails newwest from the email ids 
    for e_id in email_ids[-5:]:
        
        #Step #6 get full email format RFC822 
        result, msg_data = mail.fetch(e_id, '(RFC822)')

        #Step #7 convert raw email into readable format 
        raw_email = msg_data[0][1]

        #Step #8 convert raw email into readable format
        msg = email.message_from_bytes(raw_email)

        # decode the email
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")

        # decode sender name and email
        sender, encoding = decode_header(msg.get("From"))[0]
        if isinstance(sender, bytes):
            sender = sender.decode(encoding if encoding else "utf-8")

        #get date
        date = msg.get("Date")

        # get body preview
        body = ""
        
        #extract body if multi part
        if msg.is_multipart():

            #loop through parts     
            for part in msg.walk():
                content_type = part.get_content_type()
               
                #find plain text               
                if content_type == "text/plain":

                    #decode body
                    body = part.get_payload(decode=True).decode(errors="ignore")
                    break
        else:
            body = msg.get_payload(decode=True).decode(errors="ignore")

        print("====================================")
        print(f" Email #{count}")
        print(f" From: {sender}")
        print(f" Subject: {subject}")
        print(f" Date: {date}")
        print(f" Preview: {body[:100]}...")
        print("====================================\n")

        count += 1

    #Step #9 logout
    mail.logout()
    print("Done reading emails.")

# example usage the password needs to be the app password here too from  https://myaccount.google.com/apppasswords
read_email("lowkeymischievous@gmail.com", "ibrx juqy lako brbr")

