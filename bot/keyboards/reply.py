from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from bot.config import is_admin, WEBAPP_URL


def get_main_menu(user_id: int | None = None) -> ReplyKeyboardMarkup:
    """Asosiy menyu klaviaturasi (Universal: Ham WebApp, ham Bot tugmalari)"""
    keyboard = []

    # Agar WEBAPP_URL sozlangan bo'lsa
    if WEBAPP_URL and "vercel.app" in WEBAPP_URL or "http" in WEBAPP_URL:
        keyboard.append([
            KeyboardButton(
                text="🚀 NEXORA WebApp (Mini App)",
                web_app=WebAppInfo(url=WEBAPP_URL),
            )
        ])

    keyboard.extend([
        [
            KeyboardButton(text="🤖 Telegram bot buyurtma qilish"),
            KeyboardButton(text="🌐 Veb-sayt buyurtma qilish"),
        ],
        [
            KeyboardButton(text="🧮 Narx kalkulyatori"),
            KeyboardButton(text="📦 Mening buyurtmalarim"),
        ],
        [
            KeyboardButton(text="💰 Narxlar"),
            KeyboardButton(text="📁 Portfolio"),
        ],
        [
            KeyboardButton(text="❓ Savol-javob"),
            KeyboardButton(text="📞 Aloqa"),
        ],
    ])

    # Agar foydalanuvchi admin bo'lsa
    if user_id and is_admin(user_id):
        keyboard.append([KeyboardButton(text="⚙️ Admin panel")])

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="Quyidagi menyudan tanlang...",
    )


def get_cancel_menu() -> ReplyKeyboardMarkup:
    """FSM jarayonida bekor qilish tugmasi"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="❌ Bekor qilish")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Jarayonni bekor qilish uchun bosing...",
    )


def get_contact_menu() -> ReplyKeyboardMarkup:
    """Kontakt so'rash menyusi"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True)],
            [KeyboardButton(text="❌ Bekor qilish")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Tugmani bosing yoki raqamingizni yozing...",
    )
