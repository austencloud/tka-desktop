import os
import smtplib
from email.mime.base import MIMEBase
from email.header import Header
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr


class EmailSender:
    """A helper class to handle email sending logic."""

    @staticmethod
    def send_email(
        image_path: str,
        recipient_email: str,
        from_email: str,
        password: str,
        subject: str,
        body: str,
    ):
        msg = MIMEMultipart()
        msg["From"] = formataddr((str(Header(from_email, "utf-8")), from_email))
        msg["To"] = recipient_email
        msg["Subject"] = Header(subject, "utf-8").encode()
        msg.attach(MIMEText(body, "plain"))

        try:
            with open(image_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)

                filename = os.path.basename(image_path)
                encoded_filename = Header(filename, "utf-8").encode()

                part.add_header(
                    "Content-Disposition",
                    f'attachment; filename="{encoded_filename}"',
                )
                msg.attach(part)
        except Exception as e:
            raise Exception(f"Failed to attach image: {str(e)}")

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, recipient_email, msg.as_string())
            server.quit()
        except Exception as e:
            raise Exception(f"Failed to send email: {str(e)}")
