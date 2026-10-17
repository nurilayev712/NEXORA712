from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_admin_main_keyboard() -> InlineKeyboardMarkup:
    """Admin boshqaruv paneli tugmalari"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📊 Statistika (/stats)", callback_data="admin_stats"),
                InlineKeyboardButton(text="📦 Buyurtmalar (/orders)", callback_data="admin_orders_filter_pending"),
            ],
            [
                InlineKeyboardButton(text="📢 Xabar tarqatish (/broadcast)", callback_data="admin_broadcast"),
                InlineKeyboardButton(text="➕ Portfolio qo'shish", callback_data="admin_add_portfolio"),
            ],
        ]
    )


def get_new_order_admin_keyboard(order_id: int, user_id: int) -> InlineKeyboardMarkup:
    """Yangi buyurtma kelganda admin xabariga ulanadigan inline tugmalar"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Qabul qilish", callback_data=f"adm_accept_{order_id}"),
                InlineKeyboardButton(text="❌ Rad etish", callback_data=f"adm_reject_{order_id}"),
            ],
            [
                InlineKeyboardButton(text="⏳ Jarayonga o'tkazish", callback_data=f"adm_progress_{order_id}"),
                InlineKeyboardButton(text="👤 Mijozga yozish", url=f"tg://user?id={user_id}"),
            ],
        ]
    )


def get_orders_filter_keyboard(current_filter: str = "pending") -> InlineKeyboardMarkup:
    """Buyurtmalar holati bo'yicha filtr tugmalari"""
    statuses = [
        ("🆕 Yangi", "pending"),
        ("⏳ Jarayonda", "in_progress"),
        ("✅ Bajarilgan", "completed"),
        ("❌ Rad etilgan", "rejected"),
        ("📋 Barchasi", "all"),
    ]

    row1 = []
    row2 = []
    for label, code in statuses[:3]:
        text = f"👉 {label}" if code == current_filter else label
        row1.append(InlineKeyboardButton(text=text, callback_data=f"admin_orders_filter_{code}"))

    for label, code in statuses[3:]:
        text = f"👉 {label}" if code == current_filter else label
        row2.append(InlineKeyboardButton(text=text, callback_data=f"admin_orders_filter_{code}"))

    return InlineKeyboardMarkup(
        inline_keyboard=[
            row1,
            row2,
            [
                InlineKeyboardButton(text="🔄 Yangilash", callback_data=f"admin_orders_filter_{current_filter}"),
                InlineKeyboardButton(text="🔙 Admin menyu", callback_data="admin_main_menu"),
            ],
        ]
    )


def get_order_actions_keyboard(order_id: int, current_status: str, user_id: int) -> InlineKeyboardMarkup:
    """Alohida buyurtmani boshqarish tugmalari"""
    buttons = []

    status_row = []
    if current_status != "in_progress":
        status_row.append(
            InlineKeyboardButton(text="⏳ Jarayonga", callback_data=f"adm_set_status_{order_id}_in_progress")
        )
    if current_status != "completed":
        status_row.append(
            InlineKeyboardButton(text="✅ Bajarildi", callback_data=f"adm_set_status_{order_id}_completed")
        )
    if current_status != "rejected":
        status_row.append(
            InlineKeyboardButton(text="❌ Rad etish", callback_data=f"adm_set_status_{order_id}_rejected")
        )

    if status_row:
        buttons.append(status_row)

    buttons.append([
        InlineKeyboardButton(text="👤 Mijoz profili", url=f"tg://user?id={user_id}"),
        InlineKeyboardButton(text="🔙 Buyurtmalarga qaytish", callback_data="admin_orders_filter_all"),
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_broadcast_confirm_keyboard() -> InlineKeyboardMarkup:
    """Xabar tarqatishni tasdiqlash klaviaturasi"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🚀 Ha, barchaga yuborilsin", callback_data="broadcast_confirm"),
                InlineKeyboardButton(text="❌ Bekor qilish", callback_data="broadcast_cancel"),
            ]
        ]
    )


def get_portfolio_category_keyboard() -> InlineKeyboardMarkup:
    """Portfolio qo'shishda toifa tanlash"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🤖 Telegram bot", callback_data="addport_cat_bot"),
                InlineKeyboardButton(text="🌐 Veb-sayt", callback_data="addport_cat_website"),
            ],
            [
                InlineKeyboardButton(text="❌ Bekor qilish", callback_data="addport_cancel"),
            ],
        ]
    )
