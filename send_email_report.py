#!#!/usr/local/bin/python3

import glob
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Load .env
load_dotenv()

sender_email = os.getenv("GMAIL_SENDER")
receiver_email = os.getenv("GMAIL_RECEIVER")
password = os.getenv("GMAIL_PASSWORD")

subject = "KDP Dashboard Report 📈"
body = "Hi, attached is the latest Kindle Direct Publishing report.\n\nBest regards,\nYour Automated Bot 🤖"

# Find the latest KDP Dashboard file
downloads_folder = os.path.expanduser("~/Downloads")
report_files = glob.glob(os.path.join(downloads_folder, "KDP_Dashboard-*.xlsx"))
report_files.sort(key=os.path.getmtime, reverse=True)  # Newest first
report_path = report_files[0] if report_files else None


# Build email
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))

if report_path:
    try:
        with open(report_path, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(report_path))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(report_path)}"'
            msg.attach(part)
    except FileNotFoundError:
        print(f"⚠️ Error: Couldn't find report at {report_path}. Sending without attachment.")
else:
    print("⚠️ No report files found. Sending email without attachment.")

# Send email
try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
    print("✅ Email sent successfully!")
except Exception as e:
    print(f"❌ Failed to send email: {e}")

if not sender_email or not receiver_email or not password:
    print("❌ Missing one or more required environment variables. Exiting.")
    exit(1)

