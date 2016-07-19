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

        print part.get_payload(decode=True)

get_attachment_text()


'''SEARCH parameters - 
http://www.example-code.com/csharp/imap-search-critera.asp 
https://tools.ietf.org/html/rfc3501#section-6.4.4 
http://stackoverflow.com/questions/12944727/python-imaplib-view-message-to-specific-sender
'''