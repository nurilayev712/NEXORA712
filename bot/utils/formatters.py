STATUS_LABELS = {
    "pending": "🆕 Yangi",
    "in_progress": "⏳ Jarayonda",
    "completed": "✅ Bajarildi",
    "rejected": "❌ Bekor qilingan / Rad etilgan",
}


def get_status_badge(status: str) -> str:
    """Holat uchun emoji va nom"""
    return STATUS_LABELS.get(status, status)


def format_order_summary(data: dict) -> str:
    """Mijozga tasdiqlash uchun buyurtma xulosasi"""
    return (
        "📋 **BUYURTMA XULOSASI:**\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📌 **Xizmat turi:** {data.get('service_type', 'Noma\'lum')}\n"
        f"💡 **Loyiha nomi:** {data.get('project_name', 'Ko\'rsatilmagan')}\n"
        f"📝 **Tavsif:** {data.get('description', 'Ko\'rsatilmagan')}\n"
        f"💰 **Byudjet:** {data.get('budget', 'Ko\'rsatilmagan')}\n"
        f"⏱️ **Muddat:** {data.get('deadline', 'Ko\'rsatilmagan')}\n"
        f"📞 **Aloqa:** {data.get('contact', 'Ko\'rsatilmagan')}\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "Barcha ma'lumotlar to'g'rimi? Tasdiqlaysizmi?"
    )


def format_admin_order_notification(order_id: int, user_info: dict, data: dict) -> str:
    """Adminga yangi buyurtma haqida to'liq bildirishnoma"""
    full_name = user_info.get("full_name", "Noma'lum")
    username = f"@{user_info.get('username')}" if user_info.get("username") else "Mavjud emas"
    user_id = user_info.get("id") or user_info.get("telegram_id")

    return (
        f"🔔 **YANGI BUYURTMA QABUL QILINDI! (#ord_{order_id})**\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **Mijoz:** {full_name}\n"
        f"🔗 **Username:** {username}\n"
        f"🆔 **Telegram ID:** `{user_id}`\n\n"
        f"📌 **Xizmat turi:** {data.get('service_type')}\n"
        f"💡 **Loyiha nomi:** {data.get('project_name')}\n"
        f"📝 **Tavsif:**\n{data.get('description')}\n\n"
        f"💰 **Taxminiy byudjet:** {data.get('budget')}\n"
        f"⏱️ **Talab qilingan muddat:** {data.get('deadline')}\n"
        f"📞 **Aloqa ma'lumoti:** {data.get('contact')}\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "Quyidagi tugmalar orqali buyurtmani qabul qiling yoki rad eting:"
    )


def format_order_card(order: dict) -> str:
    """Bitta buyurtmaning batafsil kartasi (Admin ko'rishi uchun)"""
    username = f"@{order.get('user_username')}" if order.get("user_username") else "Yo'q"
    status_badge = get_status_badge(order.get("status", "pending"))

    return (
        f"📦 **Buyurtma #{order.get('id')}**\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📊 **Holati:** {status_badge}\n"
        f"👤 **Buyurtmachi:** {order.get('user_full_name')} ({username})\n"
        f"🆔 **ID:** `{order.get('user_id')}`\n"
        f"📅 **Sana:** {order.get('created_at')}\n\n"
        f"📌 **Xizmat:** {order.get('service_type')}\n"
        f"💡 **Loyiha:** {order.get('project_name')}\n"
        f"📝 **Tavsif:**\n{order.get('description')}\n\n"
        f"💰 **Byudjet:** {order.get('budget')}\n"
        f"⏱️ **Muddat:** {order.get('deadline')}\n"
        f"📞 **Aloqa:** {order.get('contact')}\n"
        "━━━━━━━━━━━━━━━━━━━━━━"
    )


def format_stats_report(stats: dict) -> str:
    """Statistika hisobotini chiroyli formatlash"""
    total_orders = stats.get("total_orders", 0)
    bot_orders = stats.get("bot_orders", 0)
    site_orders = stats.get("site_orders", 0)

    # Nisbatni hisoblash
    bot_percent = (bot_orders / total_orders * 100) if total_orders > 0 else 0
    site_percent = (site_orders / total_orders * 100) if total_orders > 0 else 0

    return (
        "📊 **NEXORA DEV - STATISTIKA HISOBOTI**\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👥 **Jami foydalanuvchilar:** {stats.get('total_users', 0):,} ta\n"
        f"📦 **Jami buyurtmalar:** {total_orders:,} ta\n"
        f"📅 **Bugungi buyurtmalar:** {stats.get('today_orders', 0):,} ta\n"
        f"🗓 **Shu oylik buyurtmalar:** {stats.get('month_orders', 0):,} ta\n\n"
        "📊 **Xizmatlar bo'yicha nisbat:**\n"
        f"• 🤖 **Telegram botlar:** {bot_orders} ta ({bot_percent:.1f}%)\n"
        f"• 🌐 **Veb-saytlar:** {site_orders} ta ({site_percent:.1f}%)\n\n"
        "📌 **Holatlar taqsimoti:**\n"
        f"• 🆕 Yangi: {stats.get('pending_orders', 0)} ta\n"
        f"• ⏳ Jarayonda: {stats.get('in_progress_orders', 0)} ta\n"
        f"• ✅ Bajarilgan: {stats.get('completed_orders', 0)} ta\n"
        f"• ❌ Rad etilgan: {stats.get('rejected_orders', 0)} ta\n"
        "━━━━━━━━━━━━━━━━━━━━━━"
    )
