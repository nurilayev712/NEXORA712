from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.config import ADMIN_USERNAME, ADMIN_PHONE
from bot.data.faq import FAQ_ITEMS


def get_budget_keyboard() -> InlineKeyboardMarkup:
    """Taxminiy byudjet tanlash inline tugmalari"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💵 $50 - $100", callback_data="budget_$50-$100"),
                InlineKeyboardButton(text="💵 $100 - $300", callback_data="budget_$100-$300"),
            ],
            [
                InlineKeyboardButton(text="💵 $300 - $500", callback_data="budget_$300-$500"),
                InlineKeyboardButton(text="💎 $500+", callback_data="budget_$500+"),
            ],
            [
                InlineKeyboardButton(text="🤝 Kelishilgan holda", callback_data="budget_Kelishilgan"),
            ],
        ]
    )


def get_deadline_keyboard() -> InlineKeyboardMarkup:
    """Muddat tanlash inline tugmalari"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⚡ 1 - 3 kun (Tezkor)", callback_data="deadline_1-3 kun"),
                InlineKeyboardButton(text="📅 3 - 7 kun", callback_data="deadline_3-7 kun"),
            ],
            [
                InlineKeyboardButton(text="📆 1 - 2 hafta", callback_data="deadline_1-2 hafta"),
                InlineKeyboardButton(text="🗓 1 oy+", callback_data="deadline_1 oy+"),
            ],
            [
                InlineKeyboardButton(text="⏳ Farqi yo'q (Kelishilgan)", callback_data="deadline_Kelishilgan"),
            ],
        ]
    )


def get_order_confirm_keyboard() -> InlineKeyboardMarkup:
    """Buyurtmani tasdiqlash yoki bekor qilish tugmalari"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="order_confirm"),
                InlineKeyboardButton(text="✏️ Qayta kiritish", callback_data="order_restart"),
            ],
            [
                InlineKeyboardButton(text="❌ Bekor qilish", callback_data="order_cancel"),
            ],
        ]
    )


def get_prices_keyboard() -> InlineKeyboardMarkup:
    """Narxlar bo'limi navigatsiyasi"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🤖 Telegram bot narxlari", callback_data="price_bot"),
                InlineKeyboardButton(text="🌐 Veb-sayt narxlari", callback_data="price_website"),
            ],
            [
                InlineKeyboardButton(text="📋 Barcha narxlar", callback_data="price_both"),
            ],
            [
                InlineKeyboardButton(text="✍️ Buyurtma berish", callback_data="order_from_price"),
            ],
        ]
    )


def get_portfolio_keyboard() -> InlineKeyboardMarkup:
    """Portfolio toifalari navigatsiyasi"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🤖 Bot loyihalari", callback_data="portfolio_bot"),
                InlineKeyboardButton(text="🌐 Veb-saytlar", callback_data="portfolio_website"),
            ],
            [
                InlineKeyboardButton(text="📂 Barchasi", callback_data="portfolio_all"),
            ],
            [
                InlineKeyboardButton(text="🚀 Loyihangizga buyurtma berish", callback_data="order_from_portfolio"),
            ],
        ]
    )


def get_faq_keyboard() -> InlineKeyboardMarkup:
    """FAQ savollari uchun inline tugmalar"""
    keyboard = []
    for item in FAQ_ITEMS:
        keyboard.append([
            InlineKeyboardButton(text=f"❓ {item['short']}", callback_data=f"faq_{item['id']}")
        ])
    keyboard.append([
        InlineKeyboardButton(text="📖 Barchasini birdaniga o'qish", callback_data="faq_read_all")
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_faq_single_keyboard() -> InlineKeyboardMarkup:
    """Bitta savol javobidagi orqaga qaytish tugmasi"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔙 Barcha savollarga qaytish", callback_data="faq_back_to_list"),
            ],
            [
                InlineKeyboardButton(text="✍️ Savol berish / Aloqa", callback_data="send_feedback_to_admin"),
            ],
        ]
    )


def get_contact_inline_keyboard() -> InlineKeyboardMarkup:
    """Aloqa bo'limi inline havolalari (Xatosiz, to'liq ishlaydigan)"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💬 Telegram orqali yozish",
                    url=f"https://t.me/{ADMIN_USERNAME}",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="✍️ Bot orqali to'g'ridan-to'g'ri murojaat yo'llash",
                    callback_data="send_feedback_to_admin",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🧮 Narx kalkulyatori",
                    callback_data="calc_start",
                ),
                InlineKeyboardButton(
                    text="🚀 Yangi buyurtma",
                    callback_data="order_from_contact",
                ),
            ],
        ]
    )


# ==================== KALKULYATOR KLAWIATURALARI ====================
def get_calc_type_keyboard() -> InlineKeyboardMarkup:
    """Kalkulyator 1-bosqich: Xizmat turi"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🤖 Telegram Bot", callback_data="calc_type_bot"),
                InlineKeyboardButton(text="🌐 Veb-sayt", callback_data="calc_type_website"),
            ],
            [
                InlineKeyboardButton(text="❌ Bekor qilish", callback_data="calc_cancel"),
            ],
        ]
    )


def get_calc_level_keyboard(service_type: str) -> InlineKeyboardMarkup:
    """Kalkulyator 2-bosqich: Loyiha murakkablik darajasi"""
    if service_type == "bot":
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🔹 Boshlang'ich (Vizitka, feedback)", callback_data="calc_lvl_basic")],
                [InlineKeyboardButton(text="⚡ O'rta (Do'kon, to'lovlar, savatcha)", callback_data="calc_lvl_medium")],
                [InlineKeyboardButton(text="🚀 Yuqori (WebApp mini ilova, CRM, API)", callback_data="calc_lvl_advanced")],
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="calc_start")],
            ]
        )
    else:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🔹 Landing Page (1 sahifali)", callback_data="calc_lvl_basic")],
                [InlineKeyboardButton(text="🏢 Korporativ / Kompaniya sayti", callback_data="calc_lvl_medium")],
                [InlineKeyboardButton(text="🛒 Internet-do'kon / Maxsus portal", callback_data="calc_lvl_advanced")],
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="calc_start")],
            ]
        )


def get_calc_features_keyboard(selected_features: list[str]) -> InlineKeyboardMarkup:
    """Kalkulyator 3-bosqich: Qo'shimcha funksiyalar (ko'p tanlovli)"""
    available = [
        ("payment", "💳 Click / Payme to'lov"),
        ("admin_panel", "⚙️ Maxsus Admin panel"),
        ("multilang", "🌐 Ko'p tillilik (Uz/Ru/En)"),
        ("ai_bot", "🧠 ChatGPT / AI yordamchi"),
        ("speed_seo", "⚡ Yuqori tezlik & SEO"),
    ]

    buttons = []
    for code, label in available:
        checked = "✅" if code in selected_features else "⬜"
        buttons.append([
            InlineKeyboardButton(text=f"{checked} {label}", callback_data=f"calc_feat_{code}")
        ])

    buttons.append([
        InlineKeyboardButton(text="💰 Hisoblash va Natija ➡️", callback_data="calc_finish"),
    ])
    buttons.append([
        InlineKeyboardButton(text="🔄 Tozalash", callback_data="calc_reset_feats"),
        InlineKeyboardButton(text="❌ Bekor qilish", callback_data="calc_cancel"),
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_calc_result_keyboard() -> InlineKeyboardMarkup:
    """Kalkulyator yakuniy natijasi tugmalari"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🚀 Ushbu hisob bilan buyurtma berish", callback_data="calc_order_now"),
            ],
            [
                InlineKeyboardButton(text="🔄 Qaytadan hisoblash", callback_data="calc_start"),
                InlineKeyboardButton(text="🏠 Asosiy menyu", callback_data="calc_cancel"),
            ],
        ]
    )

