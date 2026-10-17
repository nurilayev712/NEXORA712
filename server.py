"""
NEXORA712 - Unified Production Server (Render & 24/7 Deployment)
---------------------------------------------------------------
Ushbu server bir vaqtning o'zida:
1. Google / Web saytni (index.html, style.css, script.js) xizmat qiladi
2. Instagram Bio Link saytini (/bio -> bio.html) xizmat qiladi
3. Telegram WebApp ni (/webapp -> webapp/index.html) xizmat qiladi
4. Aiogram 3 Telegram Botni orqa fonda 24/7 uzluksiz yurgizadi
5. Render Free Web Service uhlab qolmasligi uchun /health va /ping endpointlarini beradi
6. O'z-o'zini avtomatik uyg'otuvchi (Self Keep-Alive) tizimiga ega
"""

import os
import sys
import time
import ssl
import asyncio
import logging
from pathlib import Path
from aiohttp import web, ClientSession
import certifi

# Loyiha ildiz papkasi
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Bot modullari
from bot.config import BOT_TOKEN, ADMIN_IDS, WEBAPP_URL
from bot.database import db
from bot.handlers import (
    start_router,
    sections_router,
    order_router,
    admin_router,
    calculator_router,
)
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeDefault

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("NEXORA_SERVER")

START_TIME = time.time()


# ===============================================================
# 1. HTTP HANDLERS (WEB SAYT, BIO VA WEBAPP)
# ===============================================================

async def handle_index(request: web.Request) -> web.Response:
    """Asosiy Google Web Portfolio sayti (index.html)"""
    file_path = BASE_DIR / "index.html"
    if file_path.exists():
        return web.FileResponse(file_path)
    return web.Response(text="NEXORA712 Web Portfolio", status=200)


async def handle_bio(request: web.Request) -> web.Response:
    """Instagram Bio Links sahifasi (bio.html)"""
    file_path = BASE_DIR / "bio.html"
    if file_path.exists():
        return web.FileResponse(file_path)
    return web.Response(text="NEXORA712 Bio Links", status=200)


async def handle_webapp(request: web.Request) -> web.Response:
    """Telegram WebApp ilovasi (webapp/index.html yoki webapp.html)"""
    webapp_path = BASE_DIR / "webapp" / "index.html"
    if webapp_path.exists():
        return web.FileResponse(webapp_path)
    fallback_path = BASE_DIR / "webapp.html"
    if fallback_path.exists():
        return web.FileResponse(fallback_path)
    return web.Response(text="NEXORA712 WebApp", status=200)


async def handle_health(request: web.Request) -> web.Response:
    """
    Render Free Web Service uhlab qolmasligi va
    UptimeRobot / Cron-Job monitoringi uchun Health Check endpoint
    """
    uptime = int(time.time() - START_TIME)
    bot_status = "running" if request.app.get("bot_task") and not request.app["bot_task"].done() else "idle"
    return web.json_response({
        "status": "online",
        "service": "NEXORA712 Multi-Platform",
        "bot_status": bot_status,
        "uptime_seconds": uptime,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
    })


# ===============================================================
# 2. BOT VA ORQA FON VAZIFALARI
# ===============================================================

async def setup_bot_commands(bot: Bot):
    """Telegram bot buyruqlar menyusini o'rnatish"""
    try:
        commands = [
            BotCommand(command="start", description="🤖 Botni ishga tushirish"),
            BotCommand(command="help", description="ℹ️ Qo'llanma va yordam"),
        ]
        await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())
    except Exception as e:
        logger.warning(f"Bot buyruqlarini sozlashda ogohlantirish: {e}")


async def run_bot_polling(app: web.Application):
    """Aiogram bot polling vazifasini ishga tushirish"""
    if not BOT_TOKEN or "YOUR_BOT_TOKEN" in BOT_TOKEN or "ABCdefGhIJK" in BOT_TOKEN:
        logger.warning("⚠️ BOT_TOKEN topilmadi yoki standart namunada. Bot o'chirilgan, faqat web-server ishlaydi.")
        return

    logger.info("🤖 Telegram Bot ishga tushirilmoqda...")

    # SSL xavfsizlik konteksti
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
    dp = Dispatcher(storage=MemoryStorage())

    # Routerlarni ulash
    dp.include_router(admin_router)
    dp.include_router(calculator_router)
    dp.include_router(order_router)
    dp.include_router(sections_router)
    dp.include_router(start_router)

    app["bot_instance"] = bot
    app["dispatcher_instance"] = dp

    # Ma'lumotlar bazasini initsializatsiya qilish
    try:
        await db.init_db()
        logger.info("✅ SQLite ma'lumotlar bazasi tayyor.")
    except Exception as e:
        logger.error(f"❌ Ma'lumotlar bazasi xatosi: {e}")

    # Buyruqlar menyusi
    await setup_bot_commands(bot)

    # Adminlarga xabar yuborish
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(
                chat_id=admin_id,
                text="🚀 **NEXORA DEV Server va Bot 24/7 rejimda muvaffaqiyatli ishga tushdi!**\nAdmin boshqaruvi: /admin",
            )
        except Exception:
            pass

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("⚡ Bot polling boshlandi (handle_signals=False).")
        # handle_signals=False web-server bilan ziddiyat bo'lmasligi uchun
        await dp.start_polling(bot, handle_signals=False)
    except asyncio.CancelledError:
        logger.info("Bot polling bekor qilindi.")
    except Exception as e:
        logger.error(f"Bot polling xatosi: {e}", exc_info=True)


async def run_keep_alive(app: web.Application):
    """
    Render Free Web Service uhlab qolmasligi uchun o'z-o'zini avtomatik ping qilish vazifasi.
    Har 10 daqiqada /health manziliga GET so'rovi yuboradi.
    """
    external_url = os.getenv("RENDER_EXTERNAL_URL")
    if not external_url:
        render_host = os.getenv("RENDER_EXTERNAL_HOSTNAME")
        if render_host:
            external_url = f"https://{render_host}"

    if not external_url:
        logger.info("ℹ️ RENDER_EXTERNAL_URL aniqlanmadi. Mahalliy rejimda keep-alive o'chiq.")
        return

    ping_url = f"{external_url.rstrip('/')}/health"
    logger.info(f"🔄 Avtomatik Keep-Alive yoqildi: {ping_url} har 10 daqiqada chaqiriladi.")

    await asyncio.sleep(60)  # Server to'liq ko'tarilishini kutish
    while True:
        try:
            async with ClientSession() as session:
                async with session.get(ping_url, timeout=15) as resp:
                    logger.info(f"💓 Keep-alive ping muvaffaqiyatli: {resp.status}")
        except Exception as e:
            logger.warning(f"Keep-alive ping ogohlantirish: {e}")
        await asyncio.sleep(600)  # Har 10 daqiqada (600 soniya)


# ===============================================================
# 3. SERVER LIFECYCLE (STARTUP VA CLEANUP)
# ===============================================================

async def on_startup(app: web.Application):
    """Server ishga tushganda orqa fon vazifalarini yaratish"""
    app["bot_task"] = asyncio.create_task(run_bot_polling(app))
    app["keep_alive_task"] = asyncio.create_task(run_keep_alive(app))


async def on_cleanup(app: web.Application):
    """Server to'xtaganda resurslarni xavfsiz tozalash"""
    logger.info("Server to'xtatilmoqda, orqa fon vazifalari tozalanmoqda...")
    if "keep_alive_task" in app:
        app["keep_alive_task"].cancel()
    if "bot_task" in app:
        app["bot_task"].cancel()
    if "bot_instance" in app:
        try:
            await app["bot_instance"].session.close()
        except Exception:
            pass


def create_app() -> web.Application:
    """Aiohttp veb dasturini sozlash"""
    app = web.Application()

    # Asosiy sahifalar yo'llari
    app.router.add_get("/", handle_index)
    app.router.add_get("/bio", handle_bio)
    app.router.add_get("/bio.html", handle_bio)
    app.router.add_get("/webapp", handle_webapp)
    app.router.add_get("/webapp.html", handle_webapp)
    app.router.add_get("/health", handle_health)
    app.router.add_get("/ping", handle_health)

    # WebApp papkasidagi ommaviy fayllar
    webapp_dir = BASE_DIR / "webapp"
    if webapp_dir.exists():
        app.router.add_static("/webapp", webapp_dir)

    # Ildizdagi faqat ruxsat etilgan statik fayllarni xavfsiz berish
    async def handle_static_asset(request: web.Request) -> web.Response:
        filename = request.match_info["filename"]
        # Faqat xavfsiz kengaytmalar va ruxsat berilgan fayllar
        allowed_files = {"style.css", "script.js", "logo.jpg", "favicon.ico"}
        if filename in allowed_files:
            file_path = BASE_DIR / filename
            if file_path.exists():
                return web.FileResponse(file_path)
        raise web.HTTPNotFound()

    app.router.add_get("/{filename:[a-zA-Z0-9_-]+\\.(css|js|jpg|jpeg|png|ico|svg|webp)}", handle_static_asset)

    # Lifecycle hodisalari
    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)

    return app


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    host = "0.0.0.0"
    logger.info(f"🚀 NEXORA712 Server http://{host}:{port} manzilida ishga tushmoqda...")
    app = create_app()
    web.run_app(app, host=host, port=port)
