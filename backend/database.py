from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# ✅ สร้าง engine สำหรับเชื่อม PostgreSQL
engine = create_engine(DATABASE_URL)

# ✅ Session สำหรับจัดการ connection
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Base สำหรับใช้สร้าง model
Base = declarative_base()
