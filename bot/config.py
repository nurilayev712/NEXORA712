import os
from pathlib import Path
from dotenv import load_dotenv

# Loyihaning asosiy yo'li
BASE_DIR = Path(__file__).resolve().parent

# .env faylini yuklash (bot papkasi ichidagi yoki loyiha ildizidagi .env)
env_path = BASE_DIR / ".env"
if not env_path.exists():
    env_path = BASE_DIR.parent / ".env"

load_dotenv(dotenv_path=env_path)

# Bot konfiguratsiyasi
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

# Admin ID larini qabul qilish (vergul bilan ajratilgan bo'lishi mumkin)
_admin_raw = os.getenv("ADMIN_ID", "0").strip()
ADMIN_IDS: list[int] = []
for item in _admin_raw.split(","):
    item = item.strip()
    if item.isdigit():
        ADMIN_IDS.append(int(item))

# Asosiy admin ID (birinchisi yoki 0)
PRIMARY_ADMIN_ID = ADMIN_IDS[0] if ADMIN_IDS else 0

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "NEXORA712").lstrip("@")
ADMIN_PHONE = os.getenv("ADMIN_PHONE", "+998901234567")

# Telegram WebApp havolasi (HTTPS bo'lishi shart)
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://nexora712.vercel.app").strip()

# Ma'lumotlar bazasi fayl yo'li
DB_PATH = BASE_DIR / "database" / "bot.db"


def is_admin(user_id: int) -> bool:
    """Foydalanuvchi admin yoki yo'qligini tekshirish"""
    valid_admins = [i for i in ADMIN_IDS if i > 0]
    return user_id in valid_admins


def set_primary_admin(new_admin_id: int):
    """Admin ID ni xotirada va .env faylida yangilash"""
    global PRIMARY_ADMIN_ID
    if new_admin_id not in ADMIN_IDS:
        ADMIN_IDS.append(new_admin_id)
    PRIMARY_ADMIN_ID = new_admin_id

    # .env faylini yangilash
    try:
        content = env_path.read_text(encoding="utf-8")
        if "ADMIN_ID=" in content:
            import re
            content = re.sub(r"ADMIN_ID=\d+", f"ADMIN_ID={new_admin_id}", content)
        else:
            content += f"\nADMIN_ID={new_admin_id}\n"
        env_path.write_text(content, encoding="utf-8")
    except Exception:
        pass

