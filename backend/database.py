from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import psycopg2
from dotenv import load_dotenv
from urllib.parse import urlparse

# -------------------- โหลดไฟล์ .env --------------------
# ระบุตำแหน่ง .env ให้อยู่ในโฟลเดอร์หลักของโปรเจกต์
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(env_path)

# -------------------- ดึง DATABASE_URL --------------------
DATABASE_URL = os.getenv("DATABASE_URL")

# ✅ ถ้าไม่มีใน .env ให้ใช้ค่า fallback (กันพัง)
if not DATABASE_URL:
    DATABASE_URL = "postgresql://postgres:1234@10.117.10.236:5432/Eat_Mai_Hub"

# -------------------- ตั้งค่า SQLAlchemy Engine --------------------
engine = create_engine(DATABASE_URL)

# ✅ Session สำหรับ ORM
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Base สำหรับสร้าง Model
Base = declarative_base()


# -------------------- ฟังก์ชัน ORM --------------------
def get_db():
    """ใช้ใน route ที่ต้องการ ORM (เช่น FastAPI Depends)"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------- ฟังก์ชัน psycopg2 --------------------
def get_conn():
    """ใช้ใน route ที่ต้องการ query แบบ raw SQL (cursor)"""
    try:
        result = urlparse(DATABASE_URL)
        return psycopg2.connect(
            host=result.hostname,
            database=result.path.lstrip("/"),
            user=result.username,
            password=result.password,
            port=result.port,
        )
    except Exception as e:
        print("❌ ERROR connecting PostgreSQL:", e)
        raise e


# -------------------- ทดสอบเชื่อมต่อ (optional) --------------------
if __name__ == "__main__":
    print("🔍 Checking database connection...")
    try:
        conn = get_conn()
        print("✅ psycopg2 connected successfully.")
        conn.close()
    except Exception as e:
        print("❌ psycopg2 connection failed:", e)

    try:
        with engine.connect() as connection:
            print("✅ SQLAlchemy engine connected successfully.")
    except Exception as e:
        print("❌ SQLAlchemy connection failed:", e)
