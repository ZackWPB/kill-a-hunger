import os
from dotenv import load_dotenv

load_dotenv()

# === Секретные данные из .env ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

# === Конатакты ===

# === Настройки ===
LOG_LEVEL = "INFO"
DATABSE_URL = ""