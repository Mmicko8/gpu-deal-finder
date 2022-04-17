import smtplib
import ssl
import getpass
from email.message import EmailMessage


def email(subject, message, recipient, sender, smtp_server):
    """
    Sends an email with the given subject and message to the given recipient from the given sender.

    :param subject: the subject of the email
    :param message: the contents of the email
    :param sender: the email address which will send the email
    :param recipient: the recipient of the email
    """
    port = 465  # For SSL
    password = getpass.getpass()
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender, password)

        msg = EmailMessage()
        msg.set_content(message)

        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = recipient

        server.send_message(msg)
        server.quit()
