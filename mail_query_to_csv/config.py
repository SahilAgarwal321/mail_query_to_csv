"""Local Configuration File"""

IMAP_server_address = "imap.gmail.com"
mail_id = ''
password = ''
mailbox = 'INBOX'

search_params1 = '(SUBJECT "Test")'
search_params2 = '(OR FROM "xsahil@hotmail.com" FROM "shikha.lakhani@craftsvilla.com")'

'''SEARCH parameters -
http://www.example-code.com/csharp/imap-search-critera.asp
https://tools.ietf.org/html/rfc3501#section-6.4.4
http://stackoverflow.com/questions/12944727/python-imaplib-view-message-to-specific-sender
'''

status_template = ">>[{0}] : {1} : {2}".format(mail["From"], mail["Subject"], mail["Date"])

# Database credentials -

db_username = ''
db_host = ''
db_name = ''
csv_filename = 'name.csv'
