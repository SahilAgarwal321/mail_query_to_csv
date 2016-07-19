import email, getpass, imaplib

m = imaplib.IMAP4_SSL("imap.gmail.com")
mailid = 'sahil.agarwal@craftsvilla.com'
password = getpass.getpass()
m.login(mailid, password)
m.select("INBOX") # If using other mailbox for SQL, please enter it here.


def get_attachment_text():
    resp, items = m.search(None, '(SUBJECT "Test")', '(OR FROM "xsahil@hotmail.com" FROM "shikha.lakhani@craftsvilla.com")') 
    items = items[0].split()

    for emailid in items:
        resp, data = m.fetch(emailid, "(RFC822)")
        mail = email.message_from_string(data[0][1]) # parsing the mail content to get a mail object

        # If no attachments, skip to next email.
        if mail.get_content_maintype() != 'multipart':
            continue

        print "[" + mail["From"] + "] :" + mail["Subject"]
        read_message(mail)

def read_message(mail):
    for part in mail.walk():
        # multipart are just containers, so skip.
        if part.get_content_maintype() == 'multipart':
            continue

        # is no attachment, skip.
        if part.get('Content-Disposition') is None:
            continue

        received_csv_query = part.get_payload(decode=True)
        reply_file = make_reply_csv(received_csv_query) #make it return the csv file
        send_reply_csv(reply_file, mail) #Will also have whatever returned from make_reply_csv

def make_reply_csv():
    pass

import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

def send_reply_csv(fileToSend, mail):
    msg = MIMEMultipart()
    msg["From"] = mailid
    msg["To"] = mail["From"]
    msg["Subject"] = 'Re: ' + mail["Subject"]
    msg.preamble = 'Re: ' + mail["Subject"]

    ctype, encoding = mimetypes.guess_type(fileToSend)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"

    maintype, subtype = ctype.split("/", 1)

    if maintype == "text":
        fp = open(fileToSend)
        # Note: we should handle calculating the charset
        attachment = MIMEText(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "image":
        fp = open(fileToSend, "rb")
        attachment = MIMEImage(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "audio":
        fp = open(fileToSend, "rb")
        attachment = MIMEAudio(fp.read(), _subtype=subtype)
        fp.close()
    else:
        fp = open(fileToSend, "rb")
        attachment = MIMEBase(maintype, subtype)
        attachment.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
    msg.attach(attachment)

    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login(mailid,password)
    server.sendmail(mailid, mail["From"], msg.as_string())


'''SEARCH parameters - 
http://www.example-code.com/csharp/imap-search-critera.asp 
https://tools.ietf.org/html/rfc3501#section-6.4.4 
http://stackoverflow.com/questions/12944727/python-imaplib-view-message-to-specific-sender
'''