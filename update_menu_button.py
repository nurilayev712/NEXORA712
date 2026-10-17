import asyncio
import ssl
import certifi
from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.types import MenuButtonWebApp, WebAppInfo
from bot.config import BOT_TOKEN, WEBAPP_URL

async def main():
    ctx = ssl.create_default_context(cafile=certifi.where())
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    session = AiohttpSession()
    session._connector_init["ssl"] = ctx
    
    bot = Bot(token=BOT_TOKEN, session=session)
    print("WEBAPP URL:", WEBAPP_URL)
    
    # 1. Global Menu Button yangilash
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="NEXORA WebApp",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )
    )
    
    # 2. Foydalanuvchi chatiga ham yangilash
    await bot.set_chat_menu_button(
        chat_id=5882864189,
        menu_button=MenuButtonWebApp(
            text="NEXORA WebApp",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )
    )
    print("MUVAFFAQIYATLI: Telegram Menu Button yangilandi!")
    await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
