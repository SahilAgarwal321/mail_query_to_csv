import email
import getpass
import imaplib
import config


def initialise_mail():
    '''Initialise the email client instance'''
    mail_client = imaplib.IMAP4_SSL(config.IMAP_server_address)
    mail_client.login(config.mail_id, config.password)
    mail_client.select(config.mailbox)


def get_attachment_text():
    '''Retrieves required mails that match search criteria.'''
    resp, items = mail_client.search(None, config.search_params1, config.search_params2)
    items = items[0].split()

    for emailid in items:
        resp, data = mail_client.fetch(emailid, "(RFC822)")
        mail = email.message_from_string(data[0][1])
        # parsing the mail content to get a mail object
        # If no attachments, skip to next email.
        if mail.get_content_maintype() != 'multipart':
            continue
        read_message(mail)


def read_message(mail):
    '''Parses the content of the mail and prints the query in body'''
    for part in mail.walk():
        # multipart are just containers, so skip.
        if part.get_content_maintype() == 'multipart':
            continue
        # if no attachment, skip.
        if part.get('Content-Disposition') is None:
            continue

        print config.status_template
        # print "[" + mail["From"] + "] : " + mail["Subject"] + " : " + mail["Date"]
        print part.get_payload(decode=True)


if __name__ == '__main__':
    mail_client = initialise_mail()
    get_attachment_text(mail_client)


'''SEARCH parameters -
http://www.example-code.com/csharp/imap-search-critera.asp
https://tools.ietf.org/html/rfc3501#section-6.4.4
http://stackoverflow.com/questions/12944727/python-imaplib-view-message-to-specific-sender
'''
