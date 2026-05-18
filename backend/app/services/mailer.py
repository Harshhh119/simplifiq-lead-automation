import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import aiosmtplib
from app.config import settings

async def send_report_email(recipient_email: str, recipient_name: str, company_name: str, pdf_path: str):
    message = MIMEMultipart()
    message["From"] = settings.SMTP_USER
    message["To"] = recipient_email
    message["Subject"] = f"Your Custom Performance Briefing for {company_name}"
    
    body = f"Hi {recipient_name},\n\nPlease find your attached tailored report for {company_name}.\n\nBest regards,\nSimplifIQ Team"
    message.attach(MIMEText(body, "plain"))
    
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename=SimplifIQ_{company_name}_Report.pdf")
            message.attach(part)
            
    await aiosmtplib.send(
        message, hostname=settings.SMTP_HOST, port=settings.SMTP_PORT,
        username=settings.SMTP_USER, password=settings.SMTP_PASSWORD,
        use_tls=False, start_tls=True
    )
    