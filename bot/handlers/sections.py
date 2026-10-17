from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from bot.data.prices import format_prices_text
from bot.data.faq import FAQ_ITEMS, format_all_faq_text
from bot.database import db
from bot.keyboards import (
    get_prices_keyboard,
    get_portfolio_keyboard,
    get_faq_keyboard,
    get_faq_single_keyboard,
    get_contact_inline_keyboard,
    get_cancel_menu,
    get_main_menu,
)
from bot.config import ADMIN_USERNAME, ADMIN_PHONE, ADMIN_IDS
from bot.states import FeedbackState
from bot.utils import get_status_badge

router = Router(name="sections_router")


# ==================== 1. NARXLAR ====================
@router.message(F.text == "💰 Narxlar")
async def show_prices_menu(message: Message):
    """Narxlar bo'limini ko'rsatish"""
    text = (
        "💰 **NEXORA DEV - XIZMATLAR VA NARXLAR**\n\n"
        "Biz eng yaxshi sifat va hamyonbop narxlarni taklif etamiz.\n"
        "Quyidagi tugmalar orqali alohida bot yoki veb-sayt narxlarini batafsil ko'rishingiz mumkin 👇"
    )
    await message.answer(text=text, reply_markup=get_prices_keyboard())


@router.callback_query(F.data.startswith("price_"))
async def handle_price_callback(callback: CallbackQuery):
    """Narxlar kategoriyasi tanlanganda"""
    cat = callback.data.split("_")[1]
    text = format_prices_text(category=cat)
    try:
        await callback.message.edit_text(text=text, reply_markup=get_prices_keyboard())
    except Exception:
        await callback.message.answer(text=text, reply_markup=get_prices_keyboard())
    await callback.answer()


# ==================== 2. PORTFOLIO ====================
@router.message(F.text == "📁 Portfolio")
async def show_portfolio_menu(message: Message):
    """Portfolio bo'limi"""
    portfolios = await db.get_portfolios()
    text = (
        "📁 **NEXORA DEV - BIZNING LOYIHALAR (PORTFOLIO)**\n\n"
        f"Hozirda bazamizda **{len(portfolios)} ta** muvaffaqiyatli topshirilgan loyihalar mavjud.\n"
        "Qaysi yo'nalishdagi ishlarni ko'rmoqchisiz? Quyidan toifani tanlang 👇"
    )
    await message.answer(text=text, reply_markup=get_portfolio_keyboard())


@router.callback_query(F.data.startswith("portfolio_"))
async def handle_portfolio_callback(callback: CallbackQuery):
    """Portfolio toifasi bo'yicha saralash"""
    cat = callback.data.split("_")[1]
    items = await db.get_portfolios(category=cat)

    if not items:
        await callback.answer("Bu toifada hali ishlar mavjud emas.", show_alert=True)
        return

    cat_title = "🤖 Telegram botlar" if cat == "bot" else "🌐 Veb-saytlar" if cat == "website" else "📂 Barcha ishlar"
    msg_lines = [f"📁 **PORTFOLIO: {cat_title}**\n━━━━━━━━━━━━━━━━━━━━━━\n"]

    for idx, item in enumerate(items, 1):
        link_str = f" [🔗 Havola]({item['link']})" if item.get("link") else ""
        msg_lines.append(
            f"**{idx}. {item['title']}**\n"
            f"📝 {item['description']}{link_str}\n"
        )

    msg_lines.append("━━━━━━━━━━━━━━━━━━━━━━\nSizga ham shunday loyiha kerakmi? Marhamat, buyurtma bering!")
    result_text = "\n".join(msg_lines)

    try:
        await callback.message.edit_text(result_text, reply_markup=get_portfolio_keyboard(), disable_web_page_preview=True)
    except Exception:
        await callback.message.answer(result_text, reply_markup=get_portfolio_keyboard(), disable_web_page_preview=True)

    await callback.answer()


# ==================== 3. SAVOL-JAVOB (FAQ) ====================
@router.message(F.text == "❓ Savol-javob")
async def show_faq_menu(message: Message):
    """Savol-javoblar bo'limi"""
    text = (
        "❓ **TEZ-TEZ SO'RALADIGAN SAVOLLAR (FAQ)**\n\n"
        "O'zingizni qiziqtirgan savol ustiga bosing yoki barchasini birdaniga o'qing 👇"
    )
    await message.answer(text=text, reply_markup=get_faq_keyboard())


@router.callback_query(F.data == "faq_read_all")
async def handle_faq_read_all(callback: CallbackQuery):
    """Barcha FAQ larni bitta matnda o'qish"""
    text = format_all_faq_text()
    try:
        await callback.message.edit_text(text=text, reply_markup=get_faq_single_keyboard())
    except Exception:
        await callback.message.answer(text=text, reply_markup=get_faq_single_keyboard())
    await callback.answer()


@router.callback_query(F.data == "faq_back_to_list")
async def handle_faq_back(callback: CallbackQuery):
    """FAQ ro'yxatiga qaytish"""
    text = (
        "❓ **TEZ-TEZ SO'RALADIGAN SAVOLLAR (FAQ)**\n\n"
        "O'zingizni qiziqtirgan savol ustiga bosing yoki barchasini birdaniga o'qing 👇"
    )
    try:
        await callback.message.edit_text(text=text, reply_markup=get_faq_keyboard())
    except Exception:
        await callback.message.answer(text=text, reply_markup=get_faq_keyboard())
    await callback.answer()


@router.callback_query(F.data.startswith("faq_"))
async def handle_single_faq(callback: CallbackQuery):
    """Bitta savol tanlanganda javobini ko'rsatish"""
    faq_id = callback.data.replace("faq_", "")
    item = next((f for f in FAQ_ITEMS if f["id"] == faq_id), None)

    if item:
        text = f"🔹 **{item['question']}**\n\n{item['answer']}"
        try:
            await callback.message.edit_text(text=text, reply_markup=get_faq_single_keyboard())
        except Exception:
            await callback.message.answer(text=text, reply_markup=get_faq_single_keyboard())
    await callback.answer()


# ==================== 4. ALOQA ====================
@router.message(F.text == "📞 Aloqa")
async def show_contact_info(message: Message):
    """Aloqa ma'lumotlari"""
    text = (
        "📞 **BIZ BILAN ALOQA**\n\n"
        "Savollaringiz bormi yoki g'oyangizni muhokama qilmoqchimisiz?\n"
        "Biz bilan to'g'ridan-to'g'ri bog'lanishingiz mumkin:\n\n"
        f"💬 **Telegram:** @{ADMIN_USERNAME}\n"
        f"📱 **Telefon:** `{ADMIN_PHONE}` (nusxa olish uchun bosing)\n"
        "⏰ **Ish vaqti:** Har kuni 09:00 dan 22:00 gacha\n"
        "⚡ **Javob berish vaqti:** Odatda 15 daqiqa ichida\n\n"
        "Quyidagi tugmalar orqali adminga to'g'ridan-to'g'ri yozing yoki botdan murojaat qoldiring 👇"
    )
    await message.answer(text=text, reply_markup=get_contact_inline_keyboard())


# ==================== 5. MENING BUYURTMALARIM ====================
@router.message(F.text == "📦 Mening buyurtmalarim")
async def show_my_orders(message: Message):
    """Foydalanuvchining o'z buyurtmalari ro'yxati"""
    user_id = message.from_user.id
    orders = await db.get_user_orders(user_id)

    if not orders:
        no_orders_text = (
            "📦 **SIZNING BUYURTMALARINGIZ**\n\n"
            "Sizda hali rasmiylashtirilgan buyurtmalar mavjud emas.\n\n"
            "Telegram bot yoki veb-sayt buyurtma qilish uchun quyidagi menyu tugmalaridan foydalanishingiz mumkin 👇"
        )
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🤖 Telegram bot buyurtma qilish", callback_data="order_from_price")],
                [InlineKeyboardButton(text="🌐 Veb-sayt buyurtma qilish", callback_data="order_from_price")],
            ]
        )
        await message.answer(text=no_orders_text, reply_markup=markup)
        return

    lines = [
        "📦 **SIZNING BUYURTMALARINGIZ RO'YXATI:**\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
    ]

    for ord in orders:
        badge = get_status_badge(ord["status"])
        lines.append(
            f"🆔 **Buyurtma raqami:** #{ord['id']}\n"
            f"📌 **Xizmat:** {ord['service_type']}\n"
            f"💡 **Loyiha:** {ord['project_name']}\n"
            f"💰 **Byudjet:** {ord['budget']} | ⏱️ {ord['deadline']}\n"
            f"📊 **Holati:** {badge}\n"
            f"📅 **Sana:** {ord['created_at']}\n"
            "──────────────────────"
        )

    lines.append("\n_Holat o'zgarganda bot sizga avtomatik xabar yuboradi._")
    await message.answer(text="\n".join(lines))


# ==================== 6. ADMINGA TO'G'RIDAN-TO'G'RI MUROJAAT YO'LLASH ====================
@router.callback_query(F.data == "send_feedback_to_admin")
async def start_feedback_process(callback: CallbackQuery, state: FSMContext):
    """Murojaat yo'llashni boshlash"""
    await state.clear()
    text = (
        "✍️ **ADMINGA MUROJAAT YO'LLASH**\n\n"
        "O'zingizni qiziqtirgan savol, taklif yoki g'oyangizni batafsil yozib yuboring.\n"
        "Xabaringiz to'g'ridan-to'g'ri mutaxassisimizga yetkaziladi va qisqa vaqtda javob beriladi.\n\n"
        "Xabaringizni yozing 👇"
    )
    await callback.message.answer(text=text, reply_markup=get_cancel_menu())
    await state.set_state(FeedbackState.message)
    await callback.answer()


@router.message(FeedbackState.message)
async def process_feedback_message(message: Message, state: FSMContext, bot: Bot):
    """Adminga murojaatni yetkazish"""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("Murojaat bekor qilindi.", reply_markup=get_main_menu(message.from_user.id))
        return

    user = message.from_user
    username_str = f"@{user.username}" if user.username else "Mavjud emas"

    # Adminga yuboriladigan xabar
    admin_text = (
        "📩 **YANGI MIJOZ MUROJAATI!**\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **Mijoz:** {user.full_name}\n"
        f"🔗 **Username:** {username_str}\n"
        f"🆔 **ID:** `{user.id}`\n\n"
        f"💬 **Xabar matni:**\n{message.text or '[Media fayl]'}\n"
        "━━━━━━━━━━━━━━━━━━━━━━"
    )

    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="↩️ Ushbu mijozga javob yozish", callback_data=f"reply_user_{user.id}")],
            [InlineKeyboardButton(text="👤 Profilini ochish", url=f"tg://user?id={user.id}")],
        ]
    )

    sent_any = False
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(chat_id=admin_id, text=admin_text, reply_markup=reply_markup)
            sent_any = True
        except Exception:
            pass

    await state.clear()

    if sent_any:
        await message.answer(
            "✅ **Murojaatingiz adminga yetkazildi!**\nMutaxassisimiz tez orada siz bilan bog'lanadi.",
            reply_markup=get_main_menu(user.id),
        )
    else:
        await message.answer(
            "Xabaringiz qabul qilindi. Rahmat!",
            reply_markup=get_main_menu(user.id),
        )
