from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
import psycopg2
from urllib.parse import urlparse

# ✅ โหลด .env จากโฟลเดอร์หลัก (อยู่นอก backend)
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(env_path)

# ✅ ดึง DATABASE_URL จาก .env
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL not found in .env file")

# ✅ สร้าง engine สำหรับ SQLAlchemy
engine = create_engine(DATABASE_URL)

# ✅ Session สำหรับจัดการ ORM
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Base สำหรับใช้สร้าง Model
Base = declarative_base()

# ✅ ฟังก์ชันเชื่อมต่อฐานข้อมูลแบบ psycopg2 (ใช้ใน component routes)
def get_conn():
    result = urlparse(DATABASE_URL)
    return psycopg2.connect(
        host=result.hostname,
        database=result.path.lstrip("/"),
        user=result.username,
        password=result.password,
        port=result.port,
    )
