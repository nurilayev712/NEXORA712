from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from bot.database import db
from bot.keyboards import get_main_menu

router = Router(name="start_router")


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """Start buyrug'i qabul qilinganda"""
    # Har qanday avvalgi FSM holatini tozalash
    await state.clear()

    user = message.from_user
    if user:
        # Foydalanuvchini bazaga qo'shish yoki yangilash
        await db.add_user(
            telegram_id=user.id,
            full_name=user.full_name or "Mijoz",
            username=user.username,
        )

        # Agar admin ID belgilanmagan bo'lsa, birinchi foydalanuvchini admin qilish
        from bot.config import ADMIN_IDS, set_primary_admin
        valid_admins = [i for i in ADMIN_IDS if i > 0]
        if not valid_admins:
            set_primary_admin(user.id)
            await message.answer(
                f"👑 **Siz ushbu botning asosiy admini sifatida tayinlandingiz!**\n"
                f"Sizning Telegram ID: `{user.id}`\n"
                f"Admin panel: /admin",
            )

    greeting_name = user.first_name if user else "Hurmatli mijoz"

    from bot.config import WEBAPP_URL, is_admin
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, MenuButtonWebApp

    # Telegram pastki chap burchakdagi menyu tugmasini WebApp ga ulash
    try:
        await message.bot.set_chat_menu_button(
            chat_id=user.id,
            menu_button=MenuButtonWebApp(text="NEXORA WebApp", web_app=WebAppInfo(url=WEBAPP_URL)),
        )
    except Exception:
        pass

    welcome_text = (
        f"👋 **Assalomu alaykum, {greeting_name}!**\n\n"
        "⚡ **NEXORA DEV rasmiy botiga xush kelibsiz!**\n\n"
        "Biz sizning biznesingiz uchun:\n"
        "• 🤖 **Zamonaviy Telegram botlar** (Click/Payme, WebApp, do'kon, CRM)\n"
        "• 🌐 **Professional veb-saytlar** (Landing page, korporativ sayt, portal)\n"
        "ishlab chiqamiz.\n\n"
        "Quyidagi menyu tugmalari orqali bemalol buyurtma berishingiz, "
        "narxlarni kalkulyatorda hisoblashingiz yoki portfolio bilan tanishishingiz mumkin 👇"
    )

    await message.answer(
        text=welcome_text,
        reply_markup=get_main_menu(user.id if user else None),
    )


@router.message(F.text == "❌ Bekor qilish")
async def cancel_any_action(message: Message, state: FSMContext):
    """Istalgan holatni bekor qilish va bosh menyuga qaytish"""
    current_state = await state.get_state()
    if current_state:
        await state.clear()

    await message.answer(
        "Amal bekor qilindi. Bosh menyudasiz 👇",
        reply_markup=get_main_menu(message.from_user.id if message.from_user else None),
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Yordam buyrug'i"""
    help_text = (
        "ℹ️ **NEXORA DEV BOT YORDAM BO'LIMI**\n\n"
        "🤖 **Bot imkoniyatlari:**\n"
        "• Buyurtma berish uchun menyudagi bot yoki veb-sayt tugmasini bosing.\n"
        "• '💰 Narxlar' — barcha tariflar bilan tanishing.\n"
        "• '📁 Portfolio' — biz bajargan loyihalarni ko'ring.\n"
        "• '❓ Savol-javob' — ko'p beriladigan savollarga javob oling.\n"
        "• '📞 Aloqa' — to'g'ridan-to'g'ri mutaxassis bilan bog'laning.\n\n"
        "Texnik savollar yoki buyurtma bo'yicha to'g'ridan-to'g'ri aloqa: @NEXORA712"
    )
    await message.answer(help_text, reply_markup=get_main_menu(message.from_user.id if message.from_user else None))
