from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import psycopg2
from dotenv import load_dotenv

# โหลดตัวแปรจาก .env
load_dotenv()

# ✅ ดึง DATABASE_URL จาก .env
DATABASE_URL = os.getenv("DATABASE_URL")

# ✅ ถ้าไม่มีใน .env ให้ใช้ค่า fallback (กันพัง)
if not DATABASE_URL:
    DATABASE_URL = "postgresql://postgres:1234@10.117.10.236:5432/Eat_Mai_Hub"

# ✅ สร้าง engine สำหรับเชื่อม PostgreSQL (ใช้กับ SQLAlchemy ORM)
engine = create_engine(DATABASE_URL)

# ✅ Session สำหรับจัดการ connection
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Base สำหรับใช้สร้าง model
Base = declarative_base()

# ✅ ฟังก์ชันเชื่อมต่อฐานข้อมูลโดยตรง (ใช้กับ psycopg2)
def get_conn():
    """เชื่อมต่อ PostgreSQL โดยตรง สำหรับ query แบบ raw SQL"""
    return psycopg2.connect(
        host="10.117.10.236",
        database="Eat_Mai_Hub",
        user="postgres",
        password="1234"
    )
