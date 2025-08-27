import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/eatmaihub"
)
APP_NAME = os.getenv("APP_NAME", "EatMaiHub API")
