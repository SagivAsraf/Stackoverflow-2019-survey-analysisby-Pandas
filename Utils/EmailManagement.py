import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailManagement:

    def __init__(self):
        pass

    @staticmethod
    def send_email(sender_mail, sender_password, receiver_mail, file_path):
        port = 465  # For SSL
        my_email = sender_mail
        password = sender_password
        subject = "Pandas Seminar project logs From Liran and Sagiv"
        body = "Hi, the logs of the pandas seminar is attached to this mail as txt file. :) "

        send_email_to = receiver_mail

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = my_email
        message["To"] = send_email_to
        message["Subject"] = subject
        message["Bcc"] = send_email_to

        # Add body to email
        message.attach(MIMEText(body, "plain"))

        # Open PDF file in binary mode
        with open(file_path, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

            # Encode file in ASCII characters to send by email
            encoders.encode_base64(part)

            # Add header as key/value pair to attachment part
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {file_path}",
            )

            # Add attachment to message and convert message to string
            message.attach(part)
            text = message.as_string()

        # Create a secure SSL context
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(my_email, password)
            server.sendmail(my_email, send_email_to, text)
            print("Email with the log file as attachment had been sent to: ", send_email_to)
            print("If you can't track the mail, please check in your SPAM folder. ")
