import asyncio
import logging
import sys
from pathlib import Path

# Loyiha papkasini Python path ga qo'shish
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeDefault

from bot.config import BOT_TOKEN, ADMIN_IDS
from bot.database import db
from bot.handlers import start_router, sections_router, order_router, admin_router, calculator_router


async def setup_bot_commands(bot: Bot):
    """Botning pastki menyu buyruqlarini sozlash"""
    commands = [
        BotCommand(command="start", description="🤖 Botni ishga tushirish"),
        BotCommand(command="help", description="ℹ️ Qo'llanma va yordam"),
    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())


async def main():
    """Botni ishga tushiruvchi asosiy asinxron funksiya"""
    # 1. Logging sozlamalari
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )
    logger = logging.getLogger("NexoraBot")
    logger.info("Bot ishga tushirilmoqda...")

    # 2. Token tekshiruvi
    if not BOT_TOKEN or "YOUR_BOT_TOKEN" in BOT_TOKEN or "ABCdefGhIJK" in BOT_TOKEN:
        logger.error(
            "\n"
            "===============================================================\n"
            "❌ XATOLIK: BOT_TOKEN ko'rsatilmagan yoki namuna holatida!\n"
            "Iltimos, 'bot/.env' faylini oching va @BotFather dan olingan bot tokeningizni kiriting:\n"
            "BOT_TOKEN=123456789:ABCdefGhIJK...\n"
            "ADMIN_ID=SizningTelegramIDingiz\n"
            "===============================================================\n"
        )
        return

    # 3. Ma'lumotlar bazasini initsializatsiya qilish
    try:
        await db.init_db()
        logger.info("SQLite ma'lumotlar bazasi muvaffaqiyatli ishga tushirildi.")
    except Exception as e:
        logger.error(f"Ma'lumotlar bazasini yuklashda xatolik: {e}")
        return

    # 4. SSL va Bot sessiyasini sozlash (Windows sertifikat xatolarini oldini olish)
    import ssl
    import certifi
    from aiogram.client.session.aiohttp import AiohttpSession

    try:
        ssl_ctx = ssl.create_default_context(cafile=certifi.where())
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE
    except Exception:
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE

    custom_session = AiohttpSession()
    custom_session._connector_init["ssl"] = ssl_ctx

    bot = Bot(
        token=BOT_TOKEN,
        session=custom_session,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN),
    )
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # 5. Routerlarni ulash
    # Eslatma: admin va order tartibi muhim
    dp.include_router(admin_router)
    dp.include_router(calculator_router)
    dp.include_router(order_router)
    dp.include_router(sections_router)
    dp.include_router(start_router)

    # 6. Buyruqlar menyusini o'rnatish
    await setup_bot_commands(bot)

    # 7. Adminlarga bot ishga tushganligi haqida xabar berish
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(
                chat_id=admin_id,
                text="🚀 **NEXORA DEV Bot muvaffaqiyatli ishga tushdi va xizmatga tayyor!**\nAdmin boshqaruvi: /admin",
            )
        except Exception:
            pass

    logger.info("Bot polling rejimi boshlandi. Xabarlar qabul qilinmoqda...")

    # 8. Eski kutilmagan xabarlarni tozalash va pollingni boshlash
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        logger.info("Bot to'xtatildi.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("\nBot foydalanuvchi tomonidan to'xtatildi.")
