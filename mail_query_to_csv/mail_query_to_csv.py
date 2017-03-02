import email
import imaplib
import config
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.base import MIMEBase
from email.mime.text import MIMEText


def initialise_mail():
    '''Initialise the email client instance'''
    mail_client = imaplib.IMAP4_SSL(config.IMAP_server_address)
    mail_client.login(config.mail_id, config.password)
    mail_client.select(config.mailbox)
    return mail_client


def get_attachment_text(mail_client):
    '''Retrieves required mails that match search criteria.'''
    resp, items = mail_client.search(None, config.search_params1, config.search_params2)
    items = items[0].split()

    for emailid in items:
        resp, data = mail_client.fetch(emailid, "(RFC822)")
        mail = email.message_from_string(data[0][1])
        '''parsing the mail content to get a mail object
        If no attachments, skip to next email.'''
        if mail.get_content_maintype() != 'multipart':
            continue
        read_message(mail)


def read_message(mail):
    '''Parses the content of the mail and gets query from body'''
    for part in mail.walk():
        # multipart are just containers, so skip.
        if part.get_content_maintype() == 'multipart':
            continue
        # is no attachment, skip.
        if part.get('Content-Disposition') is None:
            continue

        print config.status_template
        # print "[" + mail["From"] + "] : " + mail["Subject"] + " : " + mail["Date"]
        received_csv_query = part.get_payload(decode=True)
        csv_file = get_reply_csv(received_csv_query)
        send_reply_csv(csv_file, mail)


def get_reply_csv(received_csv_query):
    '''Sends query to database and gets back data in a csv file. Format : \n
    `mysql -u username -ppassword -h host db_name -e "query" < any_csv_filename.csv`
    '''
    csv_filename = config.csv_filename
    mysql -u config.db_username -ppassword -h config.db_host config.db_name -e received_csv_query < csv_filename
    return csv_filename


def send_reply_csv(file, mail):
    '''Sends a mail with csv "file" as reply to the recieved "mail" (which had the query)'''
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
        attachment = MIMEText(fp.read(), _subtype=subtype)
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


if __name__ == '__main__':
    mail_client = initialise_mail()
    get_attachment_text(mail_client)
