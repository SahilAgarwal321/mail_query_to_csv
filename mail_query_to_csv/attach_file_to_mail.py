'''Utility code that determines file type, attaches it to mail, sends mail.'''

import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText


def send_reply(file, mail):
    '''Sends a mail with "file" as reply to the recieved "mail"'''
    msg = MIMEMultipart()
    set_reply_msg_credentials(msg)
    attach_file(msg, file)

    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login(config.mail_id, config.password)
    server.sendmail(config.mail_id, mail["From"], msg.as_string())


def set_reply_msg_credentials(msg):
    '''Set the outgoing ie. reply mail credentials'''
    msg["From"] = config.mail_id
    msg["To"] = mail["From"]
    msg["Subject"] = 'Re: ' + mail["Subject"]
    msg.preamble = 'Re: ' + mail["Subject"]


def attach_file(msg, file):
    '''Attach the file to the mail'''
    maintype, subtype = get_file_type(file)
    if maintype == "text":
        fp = open(file)
        # Note: we should handle calculating the charset
        attachment = MIMEText(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "image":
        fp = open(file, "rb")
        attachment = MIMEImage(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "audio":
        fp = open(file, "rb")
        attachment = MIMEAudio(fp.read(), _subtype=subtype)
        fp.close()
    else:
        fp = open(file, "rb")
        attachment = MIMEBase(maintype, subtype)
        attachment.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment", filename=file)
    msg.attach(attachment)


def get_file_type(file):
    """Determines the file type based on it's URL/extension"""
    ctype, encoding = mimetypes.guess_type(file)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"
    maintype, subtype = ctype.split("/", 1)
    return maintype, subtype

