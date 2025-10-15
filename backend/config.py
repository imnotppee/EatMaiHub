from dotenv import load_dotenv
import os

load_dotenv()

MAIL_FROM = os.getenv("MAIL_FROM")
SMTP_SERVER = os.getenv("MAIL_SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("MAIL_SMTP_PORT", 587))
SMTP_USER = os.getenv("MAIL_USERNAME")
SMTP_PASS = os.getenv("MAIL_APP_PASSWORD")
OTP_SECRET = os.getenv("OTP_SECRET_KEY")
OTP_EXP_MINUTES = int(os.getenv("OTP_EXP_MINUTES", 10))
DATABASE_URL = os.getenv("DATABASE_URL")
