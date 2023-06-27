import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender_email, receiver_email, subject, message, smtp_server, smtp_port, smtp_username, smtp_password):
    # Create a multipart message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    # Add the message to the body of the email
    msg.attach(MIMEText(message, "plain"))

    # Create a SMTP session
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)

    print("Email sent successfully!")

# Example usage
sender_email = "officialark11@gmail.com"
receiver_email = "officialark11@gmail.com"
subject = "Hello from Python!"
message = "This is a test email sent using Python."
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_username = "officialark11@gmail.com"
smtp_password = "ikrazhdeoptjzrgr"


send_email(sender_email, receiver_email, subject, message, smtp_server, smtp_port, smtp_username, smtp_password)
