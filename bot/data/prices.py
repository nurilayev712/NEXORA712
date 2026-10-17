"""
💰 NEXORA DEV - Xizmatlar va narxlar konfiguratsiya fayli
Ushbu fayldagi ma'lumotlarni o'zingizga moslab osongina tahrirlashingiz mumkin!
"""

# Telegram botlar narxlari
BOT_PRICES = [
    {
        "id": "bot_basic",
        "name": "🤖 Oddiy Vizitka / Feedback Bot",
        "price": "$50 - $100",
        "deadline": "2 - 4 kun",
        "features": [
            "Foydalanuvchilardan xabar/murojaat qabul qilish",
            "Avto-javoblar va chiroyli menyu",
            "Admin bildirishnomalari",
            "Statistika",
        ],
    },
    {
        "id": "bot_shop",
        "name": "🛍️ Telegram Internet Do'kon / E-commerce Bot",
        "price": "$150 - $350",
        "deadline": "5 - 10 kun",
        "features": [
            "Katalog, mahsulotlar va toifalar",
            "Savatcha (karzinka) tizimi",
            "Click & Payme to'lov integratsiyasi",
            "Buyurtmalarni boshqarish admin paneli",
            "Lokatsiya yuborish va kuryer bildirishnomalari",
        ],
    },
    {
        "id": "bot_webapp",
        "name": "⚡ Telegram WebApp (Mini App)",
        "price": "$300 - $700",
        "deadline": "10 - 20 kun",
        "features": [
            "Telegram ichida to'laqonli veb-sayt tajribasi",
            "Zamonaviy mobil UI/UX interfeysi",
            "Real-time buyurtmalar va to'lovlar",
            "Mijoz shaxsiy kabineti",
            "Maxsus animatsiyalar va filtrlash",
        ],
    },
    {
        "id": "bot_custom",
        "name": "🧠 Maxsus CRM / API / AI Bot",
        "price": "$250+",
        "deadline": "Kelishilgan holda",
        "features": [
            "OpenAI (ChatGPT) yoki boshqa AI integratsiyalari",
            "1C, Google Sheets, CRM tizimlarga ulanish",
            "Avtomatlashtirilgan xabarnomalar va analitika",
            "Ko'p tilli qo'llab-quvvatlash",
        ],
    },
]

# Veb-saytlar narxlari
WEBSITE_PRICES = [
    {
        "id": "web_landing",
        "name": "🚀 Landing Page (Bir sahifali sayt)",
        "price": "$100 - $250",
        "deadline": "3 - 7 kun",
        "features": [
            "Yuqori konversiyali zamonaviy dizayn",
            "Mobil va planshetlarga to'liq moslashuvchanlik",
            "Tezkor yuklanish va SEO boshlang'ich sozlamalari",
            "Telegram yoki CRM ga to'g'ridan-to'g'ri ariza tushishi",
        ],
    },
    {
        "id": "web_corporate",
        "name": "🏢 Korporativ / Kompaniya Sayti",
        "price": "$300 - $600",
        "deadline": "10 - 18 kun",
        "features": [
            "Ko'p sahifali professional veb-sayt",
            "Xizmatlar, yangiliklar, jamoa va blog bo'limi",
            "Qulay boshqaruv (Admin panel)",
            "Ko'p tilli tizim (O'zbek, Rus, Ingliz)",
            "Interaktiv kalkulyator yoki fikr-mulohazalar",
        ],
    },
    {
        "id": "web_ecommerce",
        "name": "🛒 Internet Do'kon (Online Shop)",
        "price": "$500 - $1200",
        "deadline": "15 - 30 kun",
        "features": [
            "Cheksiz mahsulotlar va toifalar katalogi",
            "Click, Payme, Uzum to'lov tizimlari",
            "Mijoz shaxsiy kabineti va buyurtmalar tarixi",
            "Ombor va qoldiqlar hisob-kitobi",
            "Telegram bot va SMS xabarnomalar integratsiyasi",
        ],
    },
    {
        "id": "web_portal",
        "name": "⚙️ Maxsus Veb Ilova / Portal / CRM",
        "price": "$600+",
        "deadline": "Loyiha hajmiga qarab",
        "features": [
            "Noldan individual ishlab chiqish (Custom Development)",
            "Murakkab biznes mantiq va rollar tizimi",
            "API integratsiyalar va ma'lumotlar bazasi",
            "Yuqori xavfsizlik va tezlik",
        ],
    },
]


def format_prices_text(category: str = "both") -> str:
    """Narxlar matnini chiroyli formatda shakllantirish"""
    lines = []

    if category in ("both", "bot"):
        lines.append("🤖 **TELEGRAM BOTLAR NARXLARI:**\n")
        for item in BOT_PRICES:
            lines.append(f"📌 **{item['name']}**")
            lines.append(f"💰 **Narxi:** {item['price']}")
            lines.append(f"⏱️ **Muddati:** {item['deadline']}")
            lines.append("Imkoniyatlari:")
            for f in item["features"]:
                lines.append(f"  • {f}")
            lines.append("")

    if category in ("both", "website"):
        lines.append("🌐 **VEB-SAYTLAR NARXLARI:**\n")
        for item in WEBSITE_PRICES:
            lines.append(f"📌 **{item['name']}**")
            lines.append(f"💰 **Narxi:** {item['price']}")
            lines.append(f"⏱️ **Muddati:** {item['deadline']}")
            lines.append("Imkoniyatlari:")
            for f in item["features"]:
                lines.append(f"  • {f}")
            lines.append("")

    lines.append(
        "💡 _Eslatma: Yakuniy narx loyihangizning aniq texnik talablari va qo'shimcha imkoniyatlariga qarab belgilanadi._"
    )
    return "\n".join(lines)
