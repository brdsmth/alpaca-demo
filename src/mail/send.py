# Import smtplib for the actual sending function
import smtplib
from config.config import Config

# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(to_addr, from_addr, subject, content):
    password = (
        Config.GMAIL_SMTP_PASSWORD
    )  # or use app-specific password if 2FA is enabled

    sender_email = from_addr
    receiver_email = to_addr

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_addr

    html_part = MIMEText(content, "html")
    msg.attach(html_part)

    # Connect to Gmail's SMTP server using TLS
    try:
        # Create SMTP session
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()  # Identify yourself to the server
            server.starttls()  # Secure the connection using TLS
            server.ehlo()  # Re-identify after securing the connection

            # Log in to your Gmail account
            server.login(sender_email, password)

            # Send the email
            server.sendmail(sender_email, [receiver_email], msg.as_string())

            print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
