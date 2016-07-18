import email, getpass, imaplib, os

detach_dir = '.' # directory where to save attachments (default: current)

# connecting to the gmail imap server
m = imaplib.IMAP4_SSL("imap.gmail.com")
mailid = 'sahil.agarwal@craftsvilla.com'
m.login(mailid, getpass.getpass())
m.select("INBOX") # If using other mailbox for SQL, please enter it here.


def get_attachment_text():
    resp, items = m.search(None, '(SUBJECT "Test")', '(OR FROM "xsahil@hotmail.com" FROM "shikha.lakhani@craftsvilla.com")') 
    items = items[0].split()

    for emailid in items:
        resp, data = m.fetch(emailid, "(RFC822)")
        mail = email.message_from_string(data[0][1]) # parsing the mail content to get a mail object

        #Check if any attachments at all. If not, we skip to next email.
        if mail.get_content_maintype() != 'multipart':
            continue

        print "[" + mail["From"] + "] :" + mail["Subject"]

        for part in mail.walk():
            # multipart are just containers, so skip.
            if part.get_content_maintype() == 'multipart':
                continue

            # is no attachment, skip.
            if part.get('Content-Disposition') is None:
                continue

            print part.get_payload(decode=True)

get_attachment_text()