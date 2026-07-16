import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import os
from dotenv import load_dotenv

# Load local environment secrets
load_dotenv()

def generate_otp() -> str:
    return str(random.randint(100000, 999999))

def send_otp_email(to_email: str, otp: str) -> bool:
    """
    Sends an OTP verification email to the user.
    IfSMTP configurations are missing, throws ValueError to trigger local console logging.
    """
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port_env = os.getenv("SMTP_PORT", "587")
    smtp_port = int(smtp_port_env) if smtp_port_env.isdigit() else 587
    smtp_user = os.getenv("SMTP_EMAIL", "")
    smtp_password = os.getenv("SMTP_PASSWORD", "")
    
    if not smtp_user or not smtp_password:
        raise ValueError("SMTP credentials not configured in environment variables (.env)")
        
    subject = "SmartKYC - Login OTP Verification Code"
    body = f"""
    <html>
    <head>
        <style>
            .container {{
                font-family: Arial, sans-serif;
                padding: 20px;
                background-color: #f8fafc;
                border-radius: 8px;
                border: 1px solid #e2e8f0;
            }}
            .header {{
                color: #2563eb;
                font-size: 1.5rem;
                font-weight: bold;
                margin-bottom: 15px;
            }}
            .otp-code {{
                font-size: 2rem;
                font-weight: bold;
                color: #0f172a;
                letter-spacing: 4px;
                background-color: #e2e8f0;
                padding: 10px 20px;
                border-radius: 6px;
                display: inline-block;
                margin: 15px 0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">SmartKYC Security Verification</div>
            <p>Hello,</p>
            <p>You requested a One-Time Password (OTP) to log in to your SmartKYC account.</p>
            <p>Your verification code is:</p>
            <div class="otp-code">{otp}</div>
            <p>This code is valid for 5 minutes. Do not share this OTP with anyone.</p>
            <hr style="border: none; border-top: 1px solid #e2e8f0; margin-top: 20px;">
            <p style="font-size: 0.8rem; color: #64748b;">SmartKYC PAN & Aadhaar Identity Verification System</p>
        </div>
    </body>
    </html>
    """
    
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = to_email
    
    html_part = MIMEText(body, "html")
    msg.attach(html_part)
    
    # Send email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, to_email, msg.as_string())
        
    return True
