from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.states import OrderState
from bot.database import db
from bot.config import PRIMARY_ADMIN_ID, ADMIN_IDS
from bot.keyboards import (
    get_main_menu,
    get_cancel_menu,
    get_contact_menu,
    get_budget_keyboard,
    get_deadline_keyboard,
    get_order_confirm_keyboard,
    get_new_order_admin_keyboard,
)
import json
from bot.utils import (
    format_order_summary,
    format_admin_order_notification,
)

router = Router(name="order_router")


# ==================== WEBAPP ORQALI BUYURTMA QABUL QILISH ====================
@router.message(F.web_app_data)
async def process_webapp_order(message: Message, bot: Bot):
    """Telegram WebApp orqali to'ldirilgan buyurtmani qabul qilish"""
    raw_data = message.web_app_data.data
    try:
        data = json.loads(raw_data)
    except Exception:
        data = {}

    user = message.from_user
    if user:
        await db.add_user(
            telegram_id=user.id,
            full_name=user.full_name or "Mijoz",
            username=user.username,
        )

    service_type = data.get("service_type", "🤖 Telegram bot")
    project_name = data.get("project_name", "Noma'lum loyiha")
    description = data.get("description", "")
    budget = data.get("budget", "$100-300")
    deadline = data.get("deadline", "3-7 kun")
    contact = data.get("contact", f"@{user.username}" if (user and user.username) else str(user.id if user else ""))

    # Bazaga yozish
    order_id = await db.create_order(
        user_id=user.id if user else 0,
        service_type=service_type,
        project_name=project_name,
        description=description,
        budget=budget,
        deadline=deadline,
        contact=contact,
    )

    # Mijozga rasmiy qabul xabari
    success_msg = (
        "🎉 **BUYURTMANGIZ WEBAPP ORQALI QABUL QILINDI!**\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📦 **Buyurtma raqamingiz:** #`{order_id}`\n"
        f"📌 **Xizmat:** {service_type}\n"
        f"💡 **Loyiha:** {project_name}\n"
        f"📝 **Tavsif:** {description}\n"
        f"💰 **Byudjet:** {budget}\n"
        f"⏱️ **Muddat:** {deadline}\n"
        f"📞 **Aloqa:** {contact}\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "✅ Mutaxassisimiz tez orada siz ko'rsatgan aloqa orqali bog'lanadi. Rahmat!"
    )
    await message.answer(success_msg, reply_markup=get_main_menu(user.id if user else None))

    # Adminga to'liq bildirishnoma jo'natish
    admin_notif_text = format_admin_order_notification(
        order_id=order_id,
        user_info={
            "id": user.id if user else 0,
            "full_name": user.full_name if user else "Mijoz",
            "username": user.username if user else None,
        },
        data={
            "service_type": service_type,
            "project_name": project_name,
            "description": f"🌐 [WEBAPP ORQALI] {description}",
            "budget": budget,
            "deadline": deadline,
            "contact": contact,
        },
    )

    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(
                chat_id=admin_id,
                text=admin_notif_text,
                reply_markup=get_new_order_admin_keyboard(order_id, user.id if user else 0),
            )
        except Exception:
            pass



# ==================== 1-QADAM: BUYURTMA BOSHLASH ====================
@router.message(F.text.in_({"🤖 Telegram bot buyurtma qilish", "🌐 Veb-sayt buyurtma qilish"}))
async def start_order_process(message: Message, state: FSMContext):
    """Buyurtma berish jarayonini boshlash"""
    # Foydalanuvchi ma'lumotlarini bazada yangilash
    if message.from_user:
        await db.add_user(
            telegram_id=message.from_user.id,
            full_name=message.from_user.full_name or "Mijoz",
            username=message.from_user.username,
        )

    service_type = (
        "🤖 Telegram bot"
        if "Telegram bot" in message.text
        else "🌐 Veb-sayt"
    )

    await state.clear()
    await state.update_data(service_type=service_type)

    text = (
        f"🎯 Siz **{service_type}** xizmatini tanladingiz!\n\n"
        "1️⃣ **Loyihangiz nomi yoki asosiy g'oyasi nima?**\n"
        "_Masalan: 'Yetkazib berish xizmati boti', 'Kiyim do'koni', 'Stomatologiya klinikasi sayti'_\n\n"
        "Quyida loyiha nomini yozib yuboring:"
    )

    await message.answer(text=text, reply_markup=get_cancel_menu())
    await state.set_state(OrderState.project_name)


@router.callback_query(F.data.in_({"order_from_price", "order_from_portfolio", "order_from_contact"}))
async def order_from_inline_prompt(callback: CallbackQuery, state: FSMContext):
    """Inline tugmalardan buyurtma boshlanganda xizmat turini so'rash"""
    await state.clear()
    await callback.message.answer(
        "Qanday xizmatga buyurtma bermoqchisiz? Iltimos, quyidagi menyudan tanlang 👇",
        reply_markup=get_main_menu(callback.from_user.id),
    )
    await callback.answer()


# ==================== 2-QADAM: LOYIHA NOMI ====================
@router.message(OrderState.project_name)
async def process_project_name(message: Message, state: FSMContext):
    """Loyiha nomini qabul qilish"""
    # Agar bekor qilish tugmasi bosilsa
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("Buyurtma jarayoni bekor qilindi.", reply_markup=get_main_menu(message.from_user.id))
        return

    # Validatsiya
    if not message.text or len(message.text.strip()) < 2:
        await message.answer(
            "⚠️ Iltimos, loyiha nomini to'g'ri matn ko'rinishida yozing (kamida 2 ta belgi):"
        )
        return

    project_name = message.text.strip()
    await state.update_data(project_name=project_name)

    text = (
        "2️⃣ **Loyiha haqida batafsil tavsif bering:**\n\n"
        "Loyiha qanday vazifalarni bajarishi kerak? Qanday funksiyalar yoki sahifalar bo'lishini xohlaysiz?\n\n"
        "💡 _Qanchalik batafsil yozsangiz, loyihani shunchalik aniq tushunib baholaymiz._"
    )
    await message.answer(text=text, reply_markup=get_cancel_menu())
    await state.set_state(OrderState.description)


# ==================== 3-QADAM: TAVSIF ====================
@router.message(OrderState.description)
async def process_description(message: Message, state: FSMContext):
    """Loyiha tavsifini qabul qilish"""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("Buyurtma jarayoni bekor qilindi.", reply_markup=get_main_menu(message.from_user.id))
        return

    if not message.text or len(message.text.strip()) < 5:
        await message.answer(
            "⚠️ Iltimos, loyiha haqida batafsilroq tavsif bering (kamida 5 ta belgi):"
        )
        return

    description = message.text.strip()
    await state.update_data(description=description)

    text = (
        "3️⃣ **Loyiha uchun rejalashtirgan taxminiy byudjetingiz qancha?**\n\n"
        "Quyidagi tugmalardan birini tanlang yoki o'z byudjetingizni yozib yuboring (masalan: _$200_ yoki _3 000 000 so'm_):"
    )
    await message.answer(text=text, reply_markup=get_budget_keyboard())
    await state.set_state(OrderState.budget)


# ==================== 4-QADAM: BYUDJET ====================
@router.callback_query(OrderState.budget, F.data.startswith("budget_"))
async def process_budget_callback(callback: CallbackQuery, state: FSMContext):
    """Byudjet inline tugma orqali tanlanganda"""
    budget_value = callback.data.replace("budget_", "")
    await state.update_data(budget=budget_value)

    await callback.message.delete()
    text = (
        f"✅ Byudjet: **{budget_value}**\n\n"
        "4️⃣ **Loyihani bajarish uchun qanday muddat rejalashtirgansiz?**\n\n"
        "Quyidagi variantlardan birini tanlang yoki o'zingiz yozing:"
    )
    await callback.message.answer(text=text, reply_markup=get_deadline_keyboard())
    await state.set_state(OrderState.deadline)
    await callback.answer()


@router.message(OrderState.budget)
async def process_budget_text(message: Message, state: FSMContext):
    """Byudjet qo'lda yozilganda"""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("Buyurtma jarayoni bekor qilindi.", reply_markup=get_main_menu(message.from_user.id))
        return

    if not message.text:
        await message.answer("⚠️ Iltimos, byudjetni matn sifatida yozing yoki tugmalardan birini bosing:")
        return

    budget_value = message.text.strip()
    await state.update_data(budget=budget_value)

    text = (
        f"✅ Byudjet: **{budget_value}**\n\n"
        "4️⃣ **Loyihani bajarish uchun qanday muddat rejalashtirgansiz?**\n\n"
        "Quyidagi variantlardan birini tanlang yoki o'zingiz yozing:"
    )
    await message.answer(text=text, reply_markup=get_deadline_keyboard())
    await state.set_state(OrderState.deadline)


# ==================== 5-QADAM: MUDDAT ====================
@router.callback_query(OrderState.deadline, F.data.startswith("deadline_"))
async def process_deadline_callback(callback: CallbackQuery, state: FSMContext):
    """Muddat inline tugma orqali tanlanganda"""
    deadline_value = callback.data.replace("deadline_", "")
    await state.update_data(deadline=deadline_value)

    await callback.message.delete()
    text = (
        f"✅ Muddat: **{deadline_value}**\n\n"
        "5️⃣ **Siz bilan bog'lanishimiz uchun aloqa ma'lumotlaringizni qoldiring:**\n\n"
        "Pastdagi **'📱 Telefon raqamni yuborish'** tugmasini bosing yoki telefon raqamingizni yozib qoldiring:"
    )
    await callback.message.answer(text=text, reply_markup=get_contact_menu())
    await state.set_state(OrderState.contact)
    await callback.answer()


@router.message(OrderState.deadline)
async def process_deadline_text(message: Message, state: FSMContext):
    """Muddat matn sifatida yozilganda"""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("Buyurtma jarayoni bekor qilindi.", reply_markup=get_main_menu(message.from_user.id))
        return

    if not message.text:
        await message.answer("⚠️ Iltimos, muddatni yozing yoki tugmalardan birini bosing:")
        return

    deadline_value = message.text.strip()
    await state.update_data(deadline=deadline_value)

    text = (
        f"✅ Muddat: **{deadline_value}**\n\n"
        "5️⃣ **Siz bilan bog'lanishimiz uchun aloqa ma'lumotlaringizni qoldiring:**\n\n"
        "Pastdagi **'📱 Telefon raqamni yuborish'** tugmasini bosing yoki telefon raqamingizni yozib qoldiring:"
    )
    await message.answer(text=text, reply_markup=get_contact_menu())
    await state.set_state(OrderState.contact)


# ==================== 6-QADAM: ALOQA MA'LUMOTI ====================
@router.message(OrderState.contact, F.contact)
async def process_contact_telegram(message: Message, state: FSMContext):
    """Telegram contact tugmasi orqali yuborilganda"""
    phone_number = message.contact.phone_number
    if not phone_number.startswith("+"):
        phone_number = f"+{phone_number}"

    contact_str = f"{phone_number}"
    if message.from_user.username:
        contact_str += f" (@{message.from_user.username})"

    await state.update_data(contact=contact_str)
    await show_order_summary(message, state)


@router.message(OrderState.contact)
async def process_contact_text(message: Message, state: FSMContext):
    """Aloqa ma'lumoti matn orqali yozilganda"""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("Buyurtma jarayoni bekor qilindi.", reply_markup=get_main_menu(message.from_user.id))
        return

    if not message.text or len(message.text.strip()) < 5:
        await message.answer(
            "⚠️ Iltimos, to'g'ri telefon raqam yoki Telegram username qoldiring (kamida 5 ta belgi):"
        )
        return

    contact_str = message.text.strip()
    if message.from_user.username and f"@{message.from_user.username}" not in contact_str:
        contact_str += f" (@{message.from_user.username})"

    await state.update_data(contact=contact_str)
    await show_order_summary(message, state)


async def show_order_summary(message: Message, state: FSMContext):
    """Buyurtma xulosasini ko'rsatish va tasdiqlashni so'rash"""
    data = await state.get_data()
    summary_text = format_order_summary(data)

    await message.answer(
        text=summary_text,
        reply_markup=get_order_confirm_keyboard(),
    )
    await state.set_state(OrderState.confirmation)


# ==================== 7-QADAM: TASDIQLASH VA ADMINGA YUBORISH ====================
@router.callback_query(OrderState.confirmation, F.data == "order_confirm")
async def handle_order_confirm(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """Buyurtmani tasdiqlash"""
    data = await state.get_data()
    user = callback.from_user

    # Bazaga yozish
    order_id = await db.create_order(
        user_id=user.id,
        service_type=data.get("service_type", "Noma'lum"),
        project_name=data.get("project_name", ""),
        description=data.get("description", ""),
        budget=data.get("budget", ""),
        deadline=data.get("deadline", ""),
        contact=data.get("contact", ""),
    )

    await state.clear()

    # Mijozga bildirishnoma
    client_response = (
        f"✅ **Buyurtmangiz muvaffaqiyatli qabul qilindi!**\n\n"
        f"📦 **Buyurtma raqamingiz:** #`{order_id}`\n\n"
        "Tez orada mutaxassisimiz siz bilan ko'rsatilgan aloqa orqali bog'lanadi.\n"
        "Bizni tanlaganingiz uchun tashakkur! 🚀"
    )

    try:
        await callback.message.edit_text(client_response)
    except Exception:
        await callback.message.answer(client_response)

    # Asosiy menyuni qayta chiqarish
    await callback.message.answer(
        "Bosh menyu:",
        reply_markup=get_main_menu(user.id),
    )

    # Adminga to'liq xabarnoma yuborish
    admin_notif_text = format_admin_order_notification(
        order_id=order_id,
        user_info={
            "id": user.id,
            "full_name": user.full_name,
            "username": user.username,
        },
        data=data,
    )

    # Barcha adminlarga bildirishnoma jo'natish
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(
                chat_id=admin_id,
                text=admin_notif_text,
                reply_markup=get_new_order_admin_keyboard(order_id, user.id),
            )
        except Exception:
            pass

    await callback.answer("Buyurtmangiz qabul qilindi!")


@router.callback_query(OrderState.confirmation, F.data == "order_restart")
async def handle_order_restart(callback: CallbackQuery, state: FSMContext):
    """Qayta kiritishni boshlash"""
    data = await state.get_data()
    service_type = data.get("service_type", "🤖 Telegram bot")

    await state.clear()
    await state.update_data(service_type=service_type)

    text = (
        f"Qaytadan boshlaymiz ({service_type}).\n\n"
        "1️⃣ **Loyihangiz nomi yoki asosiy g'oyasi nima?**"
    )
    await callback.message.edit_text(text)
    await state.set_state(OrderState.project_name)
    await callback.answer("Qaytadan kiritish boshlandi")


@router.callback_query(OrderState.confirmation, F.data == "order_cancel")
async def handle_order_cancel(callback: CallbackQuery, state: FSMContext):
    """Buyurtmani bekor qilish"""
    await state.clear()
    await callback.message.edit_text("❌ Buyurtma bekor qilindi.")
    await callback.message.answer("Bosh menyudasiz 👇", reply_markup=get_main_menu(callback.from_user.id))
    await callback.answer("Bekor qilindi")
