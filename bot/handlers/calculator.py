from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.keyboards import (
    get_calc_type_keyboard,
    get_calc_level_keyboard,
    get_calc_features_keyboard,
    get_calc_result_keyboard,
    get_main_menu,
)
from bot.states import OrderState

router = Router(name="calculator_router")


class CalcState(StatesGroup):
    choosing_type = State()
    choosing_level = State()
    choosing_features = State()


PRICES_DATA = {
    "bot": {
        "basic": {"name": "Oddiy Vizitka Bot", "base_price": 70, "days": 3},
        "medium": {"name": "Internet Do'kon / E-commerce Bot", "base_price": 200, "days": 7},
        "advanced": {"name": "WebApp Mini Ilova / Murakkab Bot", "base_price": 400, "days": 15},
    },
    "website": {
        "basic": {"name": "Landing Page (Bir sahifali)", "base_price": 120, "days": 5},
        "medium": {"name": "Korporativ Kompaniya Sayti", "base_price": 350, "days": 12},
        "advanced": {"name": "Internet Do'kon / Maxsus Portal", "base_price": 600, "days": 20},
    },
}

FEATURE_PRICES = {
    "payment": {"name": "Click / Payme to'lov tizimlari", "price": 50, "days": 2},
    "admin_panel": {"name": "Maxsus Qulay Admin Panel", "price": 40, "days": 2},
    "multilang": {"name": "Ko'p tillilik tizimi (Uz/Ru/En)", "price": 30, "days": 1},
    "ai_bot": {"name": "ChatGPT / AI sun'iy intellekt ulanishi", "price": 60, "days": 2},
    "speed_seo": {"name": "Yuqori tezlik & SEO optimallashtirish", "price": 40, "days": 1},
}


@router.message(F.text == "🧮 Narx kalkulyatori")
@router.callback_query(F.data == "calc_start")
async def start_calculator(event: Message | CallbackQuery, state: FSMContext):
    """Kalkulyatorni boshlash"""
    await state.clear()
    text = (
        "🧮 **NEXORA DEV - INTERAKTIV NARX KALKULYATORI**\n\n"
        "Loyihangiz narxi va tayyor bo'lish muddatini 1 daqiqada hisoblang!\n\n"
        "Qaysi yo'nalishdagi xizmat narxini hisoblamoqchisiz? Tanlang 👇"
    )

    if isinstance(event, Message):
        await event.answer(text=text, reply_markup=get_calc_type_keyboard())
    else:
        try:
            await event.message.edit_text(text=text, reply_markup=get_calc_type_keyboard())
        except Exception:
            await event.message.answer(text=text, reply_markup=get_calc_type_keyboard())
        await event.answer()

    await state.set_state(CalcState.choosing_type)


@router.callback_query(F.data.in_({"calc_type_bot", "calc_type_website"}))
async def process_calc_type(callback: CallbackQuery, state: FSMContext):
    """Xizmat turi tanlanganda"""
    service_type = "bot" if callback.data == "calc_type_bot" else "website"
    await state.update_data(calc_type=service_type, selected_features=[])

    type_name = "🤖 Telegram Bot" if service_type == "bot" else "🌐 Veb-sayt"
    text = (
        f"Tanlangan xizmat: **{type_name}**\n\n"
        "Loyihangiz murakkablik darajasini tanlang 👇"
    )
    await callback.message.edit_text(text=text, reply_markup=get_calc_level_keyboard(service_type))
    await state.set_state(CalcState.choosing_level)
    await callback.answer()


@router.callback_query(F.data.startswith("calc_lvl_"))
async def process_calc_level(callback: CallbackQuery, state: FSMContext):
    """Daraja tanlanganda"""
    level = callback.data.replace("calc_lvl_", "")
    await state.update_data(calc_level=level)

    data = await state.get_data()
    selected_features = data.get("selected_features", [])

    text = (
        "⚡ **Qo'shimcha qanday imkoniyatlar kerak bo'ladi?**\n"
        "Kerakli variantlarni birma-bir bosing (belgilang):\n\n"
        "_Tugmalarni bosib ✅ qilgach, pastdagi '💰 Hisoblash' tugmasini bosing._"
    )
    await callback.message.edit_text(text=text, reply_markup=get_calc_features_keyboard(selected_features))
    await state.set_state(CalcState.choosing_features)
    await callback.answer()


@router.callback_query(F.data.startswith("calc_feat_"))
async def toggle_calc_feature(callback: CallbackQuery, state: FSMContext):
    """Qo'shimcha imkoniyatni yoqish / o'chirish"""
    feature = callback.data.replace("calc_feat_", "")
    data = await state.get_data()
    selected_features = data.get("selected_features", [])

    if feature in selected_features:
        selected_features.remove(feature)
    else:
        selected_features.append(feature)

    await state.update_data(selected_features=selected_features)

    try:
        await callback.message.edit_reply_markup(reply_markup=get_calc_features_keyboard(selected_features))
    except Exception:
        pass
    await callback.answer()


@router.callback_query(F.data == "calc_reset_feats")
async def reset_calc_features(callback: CallbackQuery, state: FSMContext):
    """Tanlangan imkoniyatlarni tozalash"""
    await state.update_data(selected_features=[])
    try:
        await callback.message.edit_reply_markup(reply_markup=get_calc_features_keyboard([]))
    except Exception:
        pass
    await callback.answer("Tozalandi")


@router.callback_query(F.data == "calc_finish")
async def finish_calculation(callback: CallbackQuery, state: FSMContext):
    """Yakuniy hisob-kitobni chiqarish"""
    data = await state.get_data()
    calc_type = data.get("calc_type", "bot")
    calc_level = data.get("calc_level", "medium")
    selected_features = data.get("selected_features", [])

    base_info = PRICES_DATA[calc_type][calc_level]
    total_price = base_info["base_price"]
    total_days = base_info["days"]

    lines = [
        "📊 **HISOB-KITOB NATIJASI:**\n" "━━━━━━━━━━━━━━━━━━━━━━",
        f"📌 **Asosiy tarif:** {base_info['name']}",
        f"💵 Boshlang'ich narx: **${base_info['base_price']}**",
        "",
    ]

    if selected_features:
        lines.append("⚙️ **Tanlangan qo'shimchalar:**")
        for f in selected_features:
            feat_info = FEATURE_PRICES[f]
            total_price += feat_info["price"]
            total_days += feat_info["days"]
            lines.append(f"• {feat_info['name']} (+${feat_info['price']})")
        lines.append("")

    som_price = total_price * 12800  # Taxminiy so'mdagi kurs
    lines.extend([
        "━━━━━━━━━━━━━━━━━━━━━━",
        f"💰 **JAMI TAXMINIY NARX:** **${total_price}** (~{som_price:,.0f} so'm)",
        f"⏱️ **TAXMINIY TAYYOR BO'LISH MUDDATI:** **{total_days} - {total_days + 3} kun**",
        "━━━━━━━━━━━━━━━━━━━━━━\n",
        "Ushbu loyiha bo'yicha to'g'ridan-to'g'ri buyurtma bermoqchimisiz? Quyidagi tugmani bosing 👇",
    ])

    await state.update_data(
        final_price=f"${total_price}",
        final_days=f"{total_days}-{total_days + 3} kun",
        calculated_title=f"{base_info['name']}",
    )

    await callback.message.edit_text(text="\n".join(lines), reply_markup=get_calc_result_keyboard())
    await callback.answer()


@router.callback_query(F.data == "calc_order_now")
async def order_from_calculated_result(callback: CallbackQuery, state: FSMContext):
    """Kalkulyator natijasi bilan to'g'ridan-to'g'ri buyurtma berish"""
    data = await state.get_data()
    calc_type = data.get("calc_type", "bot")
    service_type = "🤖 Telegram bot" if calc_type == "bot" else "🌐 Veb-sayt"
    title = data.get("calculated_title", "Loyiha")
    price = data.get("final_price", "$100-300")
    days = data.get("final_days", "5-7 kun")

    # OrderState ga o'tkazish
    await state.clear()
    await state.update_data(
        service_type=service_type,
        project_name=f"{title} (Kalkulyatordan)",
        budget=price,
        deadline=days,
    )

    text = (
        f"🚀 **Kalkulyatordan buyurtma rasmiylashtirish**\n\n"
        f"📌 Xizmat: **{service_type}**\n"
        f"💰 Byudjet: **{price}**\n"
        f"⏱️ Muddat: **{days}**\n\n"
        "2️⃣ **Loyihangiz haqida batafsilroq tavsif bering:**\n"
        "(Qanday qo'shimcha istaklaringiz bor? Yozib qoldiring)"
    )
    from bot.keyboards import get_cancel_menu
    await callback.message.edit_text(text)
    await callback.message.answer("Quyida tavsifni yozing 👇", reply_markup=get_cancel_menu())
    await state.set_state(OrderState.description)
    await callback.answer()


@router.callback_query(F.data == "calc_cancel")
async def cancel_calc(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Kalkulyator yopildi.")
    await callback.message.answer("Asosiy menyudasiz 👇", reply_markup=get_main_menu(callback.from_user.id))
    await callback.answer()
