import asyncio
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.filters import IsAdminFilter
from bot.database import db
from bot.states import BroadcastState, AddPortfolioState, AdminReplyState
from bot.utils import (
    format_stats_report,
    format_order_card,
    get_status_badge,
)
from bot.keyboards import (
    get_admin_main_keyboard,
    get_orders_filter_keyboard,
    get_order_actions_keyboard,
    get_broadcast_confirm_keyboard,
    get_portfolio_category_keyboard,
    get_main_menu,
)

router = Router(name="admin_router")
# Ushbu routerdagi barcha xabarlar va callbacklar faqat adminlar uchun
router.message.filter(IsAdminFilter())
router.callback_query.filter(IsAdminFilter())


# ==================== 1. ADMIN BOSHQARUV MENYUSI ====================
@router.message(Command("admin"))
@router.message(F.text == "⚙️ Admin panel")
async def cmd_admin_menu(message: Message, state: FSMContext):
    """Admin boshqaruv panelini ochish"""
    await state.clear()
    text = (
        "👑 **NEXORA DEV - ADMIN BOSHQARUV PANELI**\n\n"
        "Quyidagi boshqaruv buyruqlaridan foydalanishingiz mumkin:\n"
        "• 📊 **Statistika** — `/stats`\n"
        "• 📦 **Buyurtmalar** — `/orders`\n"
        "• 📢 **Xabar tarqatish** — `/broadcast`\n"
        "• ➕ **Portfolio qo'shish**\n\n"
        "Kerakli bo'limni tanlang 👇"
    )
    await message.answer(text=text, reply_markup=get_admin_main_keyboard())


@router.callback_query(F.data == "admin_main_menu")
async def cb_admin_main_menu(callback: CallbackQuery, state: FSMContext):
    """Admin menyusiga qaytish"""
    await state.clear()
    text = (
        "👑 **NEXORA DEV - ADMIN BOSHQARUV PANELI**\n\n"
        "Kerakli bo'limni tanlang 👇"
    )
    try:
        await callback.message.edit_text(text=text, reply_markup=get_admin_main_keyboard())
    except Exception:
        await callback.message.answer(text=text, reply_markup=get_admin_main_keyboard())
    await callback.answer()


# ==================== 2. STATISTIKA (/stats) ====================
@router.message(Command("stats"))
@router.callback_query(F.data == "admin_stats")
async def show_admin_statistics(event: Message | CallbackQuery):
    """Statistika hisobotini ko'rsatish"""
    stats = await db.get_stats()
    text = format_stats_report(stats)

    reply_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Yangilash", callback_data="admin_stats")],
            [InlineKeyboardButton(text="🔙 Admin panel", callback_data="admin_main_menu")],
        ]
    )

    if isinstance(event, Message):
        await event.answer(text=text, reply_markup=reply_kb)
    else:
        try:
            await event.message.edit_text(text=text, reply_markup=reply_kb)
        except Exception:
            await event.message.answer(text=text, reply_markup=reply_kb)
        await event.answer()


# ==================== 3. BUYURTMALAR (/orders) ====================
@router.message(Command("orders"))
async def cmd_orders(message: Message):
    """Buyurtmalar ro'yxatini ochish (default: pending)"""
    await render_orders_list(message, filter_status="pending")


@router.callback_query(F.data.startswith("admin_orders_filter_"))
async def cb_orders_filter(callback: CallbackQuery):
    """Filtr bo'yicha buyurtmalarni ko'rsatish"""
    status = callback.data.replace("admin_orders_filter_", "")
    await render_orders_list(callback, filter_status=status)
    await callback.answer()


async def render_orders_list(event: Message | CallbackQuery, filter_status: str):
    """Buyurtmalar ro'yxati interfeysini shakllantirish"""
    orders = await db.get_orders(status=filter_status, limit=10)
    filter_label = get_status_badge(filter_status) if filter_status != "all" else "Barchasi"

    if not orders:
        text = (
            f"📦 **BUYURTMALAR RO'YXATI ({filter_label})**\n\n"
            "Ushbu bo'limda hozircha buyurtmalar mavjud emas."
        )
        markup = get_orders_filter_keyboard(current_filter=filter_status)
    else:
        text = (
            f"📦 **BUYURTMALAR RO'YXATI ({filter_label})**\n"
            f"Jami ko'rsatilmoqda: {len(orders)} ta\n\n"
            "Batafsil ma'lumot va boshqarish uchun buyurtma tugmasini bosing 👇"
        )
        # Har bir buyurtma uchun inline tugma
        buttons = []
        for ord in orders:
            badge = get_status_badge(ord['status'])
            btn_text = f"#{ord['id']} | {ord['service_type'][:12]} | {badge}"
            buttons.append([InlineKeyboardButton(text=btn_text, callback_data=f"adm_view_order_{ord['id']}")])

        # Filtr tugmalarini qo'shish
        filter_markup = get_orders_filter_keyboard(current_filter=filter_status)
        buttons.extend(filter_markup.inline_keyboard)
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    if isinstance(event, Message):
        await event.answer(text=text, reply_markup=markup)
    else:
        try:
            await event.message.edit_text(text=text, reply_markup=markup)
        except Exception:
            await event.message.answer(text=text, reply_markup=markup)


# Bitta buyurtmani ko'rish
@router.callback_query(F.data.startswith("adm_view_order_"))
async def cb_view_single_order(callback: CallbackQuery):
    order_id = int(callback.data.replace("adm_view_order_", ""))
    order = await db.get_order(order_id)

    if not order:
        await callback.answer("Buyurtma topilmadi!", show_alert=True)
        return

    text = format_order_card(order)
    markup = get_order_actions_keyboard(
        order_id=order["id"],
        current_status=order["status"],
        user_id=order["user_id"],
    )

    try:
        await callback.message.edit_text(text=text, reply_markup=markup)
    except Exception:
        await callback.message.answer(text=text, reply_markup=markup)
    await callback.answer()


# Buyurtma statusini o'zgartirish (tezkor yoki boshqaruv orqali)
@router.callback_query(F.data.startswith("adm_accept_"))
async def cb_quick_accept(callback: CallbackQuery, bot: Bot):
    order_id = int(callback.data.replace("adm_accept_", ""))
    await change_status_and_notify(order_id, "in_progress", callback, bot, "✅ Buyurtma qabul qilindi va jarayonga o'tkazildi.")


@router.callback_query(F.data.startswith("adm_reject_"))
async def cb_quick_reject(callback: CallbackQuery, bot: Bot):
    order_id = int(callback.data.replace("adm_reject_", ""))
    await change_status_and_notify(order_id, "rejected", callback, bot, "❌ Buyurtma rad etildi.")


@router.callback_query(F.data.startswith("adm_progress_"))
async def cb_quick_progress(callback: CallbackQuery, bot: Bot):
    order_id = int(callback.data.replace("adm_progress_", ""))
    await change_status_and_notify(order_id, "in_progress", callback, bot, "⏳ Buyurtma jarayonga o'tkazildi.")


@router.callback_query(F.data.startswith("adm_set_status_"))
async def cb_set_status_detailed(callback: CallbackQuery, bot: Bot):
    parts = callback.data.split("_")
    order_id = int(parts[3])
    new_status = parts[4]

    await change_status_and_notify(
        order_id,
        new_status,
        callback,
        bot,
        f"Buyurtma holati yangilandi: {get_status_badge(new_status)}",
    )


async def change_status_and_notify(order_id: int, new_status: str, callback: CallbackQuery, bot: Bot, notice: str):
    """Statusni yangilash va mijozga bildirishnoma yuborish"""
    await db.update_order_status(order_id, new_status)
    order = await db.get_order(order_id)

    status_messages = {
        "in_progress": "Sizning buyurtmangiz **ishlab chiqish jarayoniga o'tkazildi** ⏳. Tez orada mutaxassisimiz siz bilan bog'lanadi.",
        "completed": "Sizning buyurtmangiz **muvaffaqiyatli yakunlandi va topshirildi** ✅! Biz bilan hamkorlik qilganingiz uchun rahmat.",
        "rejected": "Sizning buyurtmangiz **bekor qilindi / rad etildi** ❌. Qo'shimcha ma'lumot uchun adminga murojaat qilishingiz mumkin: @NEXORA712",
    }

    # Mijozga bildirishnoma jo'natish
    if order and order.get("user_id"):
        client_text = (
            f"🔔 **BUYURTMA HOLATI YANGILANDI!**\n\n"
            f"📦 Buyurtma: #`{order_id}`\n"
            f"Yangi holat: **{get_status_badge(new_status)}**\n\n"
            f"{status_messages.get(new_status, '')}"
        )
        try:
            await bot.send_message(chat_id=order["user_id"], text=client_text)
        except Exception:
            pass

    await callback.answer(notice, show_alert=True)

    # Xabarni yangilab qo'yish
    if order:
        order["status"] = new_status
        card_text = format_order_card(order)
        markup = get_order_actions_keyboard(order["id"], new_status, order["user_id"])
        try:
            await callback.message.edit_text(text=card_text, reply_markup=markup)
        except Exception:
            pass


# ==================== 4. XABAR TARQATISH (/broadcast) ====================
@router.message(Command("broadcast"))
@router.callback_query(F.data == "admin_broadcast")
async def start_broadcast(event: Message | CallbackQuery, state: FSMContext):
    """Xabar tarqatish jarayonini boshlash"""
    await state.clear()
    text = (
        "📢 **BARCHA FOYDALANUVCHILARGA XABAR TARQATISH**\n\n"
        "Yubormoqchi bo'lgan xabaringizni yozing (matn, rasm, video yoki havola bo'lishi mumkin).\n\n"
        "Bekor qilish uchun pastdagi '❌ Bekor qilish' tugmasini bosing:"
    )

    if isinstance(event, Message):
        await event.answer(text=text, reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="❌ Bekor qilish", callback_data="admin_main_menu")]]
        ))
    else:
        try:
            await event.message.edit_text(text=text, reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="❌ Bekor qilish", callback_data="admin_main_menu")]]
            ))
        except Exception:
            await event.message.answer(text=text)
        await event.answer()

    await state.set_state(BroadcastState.message)


@router.message(BroadcastState.message)
async def process_broadcast_message(message: Message, state: FSMContext):
    """Tarqatiladigan xabarni qabul qilish va tasdiqlashni so'rash"""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("Xabar tarqatish bekor qilindi.", reply_markup=get_admin_main_keyboard())
        return

    # Xabar ma'lumotlarini saqlash
    await state.update_data(
        broadcast_chat_id=message.chat.id,
        broadcast_message_id=message.message_id,
    )

    users_count = await db.get_users_count()

    prompt_text = (
        f"🔍 **XABARNI KO'RIB CHIQISH (PREVIEW):**\n"
        f"Ushbu xabar jami **{users_count} ta** foydalanuvchiga yuboriladi.\n\n"
        "Haqiqatan ham barcha foydalanuvchilarga yuborilsinmi?"
    )

    await message.reply(text=prompt_text, reply_markup=get_broadcast_confirm_keyboard())
    await state.set_state(BroadcastState.confirmation)


@router.callback_query(BroadcastState.confirmation, F.data == "broadcast_confirm")
async def execute_broadcast(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """Xabarni barcha foydalanuvchilarga yuborish"""
    data = await state.get_data()
    from_chat_id = data.get("broadcast_chat_id")
    msg_id = data.get("broadcast_message_id")

    await state.clear()
    await callback.message.edit_text("⏳ Xabar barcha foydalanuvchilarga yuborilmoqda, kuting...")

    users = await db.get_all_users()
    success_count = 0
    fail_count = 0

    for u in users:
        target_id = u["telegram_id"]
        try:
            await bot.copy_message(
                chat_id=target_id,
                from_chat_id=from_chat_id,
                message_id=msg_id,
            )
            success_count += 1
            await asyncio.sleep(0.04)  # Telegram flood limitini chetlab o'tish
        except Exception:
            fail_count += 1

    report_text = (
        "📢 **XABAR TARQATISH YAKUNLANDI!**\n\n"
        f"✅ Muvaffaqiyatli yetkazildi: **{success_count} ta**\n"
        f"❌ Yetib bormadi (bloklaganlar): **{fail_count} ta**\n"
        f"📊 Jami foydalanuvchilar: **{len(users)} ta**"
    )

    await callback.message.answer(text=report_text, reply_markup=get_admin_main_keyboard())
    await callback.answer()


@router.callback_query(BroadcastState.confirmation, F.data == "broadcast_cancel")
async def cancel_broadcast(callback: CallbackQuery, state: FSMContext):
    """Xabar tarqatishni bekor qilish"""
    await state.clear()
    await callback.message.edit_text("❌ Xabar tarqatish bekor qilindi.")
    await callback.message.answer("Admin boshqaruv paneli:", reply_markup=get_admin_main_keyboard())
    await callback.answer("Bekor qilindi")


# ==================== 5. PORTFOLIO QO'SHISH ====================
@router.callback_query(F.data == "admin_add_portfolio")
async def start_add_portfolio(callback: CallbackQuery, state: FSMContext):
    """Yangi portfolio qo'shishni boshlash"""
    await state.clear()
    text = (
        "➕ **YANGI PORTFOLIO QO'SHISH**\n\n"
        "Loyiha qaysi toifaga tegishli? Tanlang 👇"
    )
    await callback.message.edit_text(text=text, reply_markup=get_portfolio_category_keyboard())
    await state.set_state(AddPortfolioState.category)
    await callback.answer()


@router.callback_query(AddPortfolioState.category, F.data.startswith("addport_cat_"))
async def process_portfolio_category(callback: CallbackQuery, state: FSMContext):
    category = callback.data.replace("addport_cat_", "")
    await state.update_data(category=category)

    await callback.message.edit_text(
        f"Toifa: **{category.upper()}**\n\n"
        "1️⃣ **Loyiha nomini kiriting:**\n"
        "(Masalan: _'Choyxona Delivery Bot'_ yoki _'Logistika veb-sayti'_)"
    )
    await state.set_state(AddPortfolioState.title)
    await callback.answer()


@router.callback_query(AddPortfolioState.category, F.data == "addport_cancel")
async def cancel_portfolio_add(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("❌ Portfolio qo'shish bekor qilindi.")
    await callback.message.answer("Admin menyu:", reply_markup=get_admin_main_keyboard())
    await callback.answer("Bekor qilindi")


@router.message(AddPortfolioState.title)
async def process_portfolio_title(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Loyiha nomini matn sifatida yuboring:")
        return

    await state.update_data(title=message.text.strip())
    await message.answer(
        "2️⃣ **Loyiha haqida qisqa tavsif kiriting:**\n"
        "(Masalan: _'Kompaniya xizmatlari haqida ma'lumot beruvchi va buyurtma oluvchi zamonaviy bot.'_)"
    )
    await state.set_state(AddPortfolioState.description)


@router.message(AddPortfolioState.description)
async def process_portfolio_desc(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Tavsifni matn sifatida yuboring:")
        return

    await state.update_data(description=message.text.strip())
    await message.answer(
        "3️⃣ **Loyiha havolasini (link) kiriting:**\n"
        "(Masalan: _https://t.me/example_bot_ yoki _https://example.com_\nAgar havola bo'lmasa, **yo'q** deb yozing)"
    )
    await state.set_state(AddPortfolioState.link)


@router.message(AddPortfolioState.link)
async def process_portfolio_link(message: Message, state: FSMContext):
    link_text = message.text.strip() if message.text else ""
    link_val = None if link_text.lower() in ("yo'q", "yoq", "no", "-") else link_text

    data = await state.get_data()
    await state.clear()

    # Bazaga qo'shish
    new_id = await db.add_portfolio(
        title=data["title"],
        category=data["category"],
        description=data["description"],
        link=link_val,
    )

    success_text = (
        "✅ **YANGI PORTFOLIO MUVAFFAQIYATLI QO'SHILDI!**\n\n"
        f"🆔 ID: #{new_id}\n"
        f"📌 Nomi: {data['title']}\n"
        f"🏷 Toifa: {data['category']}\n"
        f"📝 Tavsif: {data['description']}\n"
        f"🔗 Havola: {link_val or 'Yo\'q'}\n\n"
        "Mijozlar endi ushbu loyihani '📁 Portfolio' bo'limida ko'rishlari mumkin!"
    )

    await message.answer(text=success_text, reply_markup=get_admin_main_keyboard())


# ==================== 6. MIJOZGA JAVOB YOZISH ====================
@router.callback_query(F.data.startswith("reply_user_"))
async def start_reply_to_user(callback: CallbackQuery, state: FSMContext):
    """Mijozga javob yozishni boshlash"""
    target_id = int(callback.data.replace("reply_user_", ""))
    await state.clear()
    await state.update_data(target_user_id=target_id)

    cancel_btn = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="❌ Bekor qilish", callback_data="admin_main_menu")]]
    )

    await callback.message.reply(
        f"✍️ ID `{target_id}` bo'lgan mijozga yubormoqchi bo'lgan javob xabaringizni yozing:\n"
        "(Matn, rasm yoki xabar)",
        reply_markup=cancel_btn,
    )
    await state.set_state(AdminReplyState.message)
    await callback.answer()


@router.message(AdminReplyState.message)
async def send_reply_to_user(message: Message, state: FSMContext, bot: Bot):
    """Admin javobini mijozga yetkazish"""
    data = await state.get_data()
    target_id = data.get("target_user_id")

    if not target_id:
        await state.clear()
        await message.answer("Xatolik: Mijoz aniqlanmadi.", reply_markup=get_admin_main_keyboard())
        return

    text_to_user = (
        "💬 **NEXORA DEV MUTAXASSISIDAN JAVOB:**\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{message.text or '[Fayl/Xabar]'}\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "_Savollaringiz bo'lsa, '📞 Aloqa' bo'limi orqali yana murojaat qilishingiz mumkin._"
    )

    try:
        await bot.send_message(chat_id=target_id, text=text_to_user)
        await message.answer(f"✅ Javob mijozga (ID: `{target_id}`) yetkazildi!", reply_markup=get_admin_main_keyboard())
    except Exception as e:
        await message.answer(f"❌ Xatolik yuz berdi (mijoz botni bloklagan bo'lishi mumkin): {e}", reply_markup=get_admin_main_keyboard())

    await state.clear()

