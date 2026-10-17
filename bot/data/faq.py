"""
❓ Tez-tez so'raladigan savollar va javoblar (FAQ)
"""

FAQ_ITEMS = [
    {
        "id": "faq_order",
        "question": "1️⃣ Buyurtma qanday topshiriladi va to'lov shartlari qanday?",
        "short": "Buyurtma berish va to'lov tartibi",
        "answer": (
            "Buyurtma berish juda oddiy:\n"
            "1. Botdagi **'🤖 Telegram bot buyurtma qilish'** yoki **'🌐 Veb-sayt buyurtma qilish'** tugmasini bosing.\n"
            "2. Qisqa savollarga javob bering (g'oya, byudjet, muddat va aloqa).\n"
            "3. Mutaxassisimiz siz bilan bog'lanib, texnik topshiriqni (TZ) aniqlashtiradi.\n\n"
            "💳 **To'lov tartibi:** Odatda 30-50% oldindan to'lov (avans) qilinadi, qolgan qismi esa loyiha to'liq tayyor bo'lib, tekshirib qabul qilingandan so'ng to'lanadi."
        ),
    },
    {
        "id": "faq_time",
        "question": "2️⃣ Loyiha qancha vaqtda tayyor bo'ladi?",
        "short": "Tayyor bo'lish muddatlari",
        "answer": (
            "Loyiha murakkabligiga qarab muddatlar farq qiladi:\n"
            "• Oddiy bot yoki Landing Page: **2 - 5 ish kuni**\n"
            "• Internet-do'kon boti yoki Korporativ sayt: **7 - 14 ish kuni**\n"
            "• Katta WebApp yoki murakkab CRM tizimlar: **2 - 4 hafta**\n\n"
            "Biz har bir bosqich bo'yicha mijozga doimiy hisobot berib boramiz."
        ),
    },
    {
        "id": "faq_support",
        "question": "3️⃣ Loyihani topshirgach bepul qo'llab-quvvatlash (kafolat) bormi?",
        "short": "Kafolat va texnik ko'mak",
        "answer": (
            "✅ **Ha, albatta!**\n"
            "Barcha yaratilgan bot va veb-saytlar uchun **1 oydan 3 oygacha BEPUL texnik kafolat** beramiz.\n"
            "Bu davr mobaynida yuzaga kelgan har qanday texnik xatoliklar (baglar) bepul bartaraf etiladi va foydalanish bo'yicha yo'riqnoma beriladi."
        ),
    },
    {
        "id": "faq_hosting",
        "question": "4️⃣ Server, domen va hosting masalalarida yordam berasizmi?",
        "short": "Server va hosting sozlash",
        "answer": (
            "Ha! Botni 24/7 o'chmasdan ishlashi uchun VPS serverga o'rnatib, sozlab beramiz.\n"
            "Saytlar uchun esa domen (.uz, .com) olish va zamonaviy xavfsiz hostingga (yoki Vercel/VPS) joylashni to'liq o'z zimmamizga olamiz."
        ),
    },
    {
        "id": "faq_payments",
        "question": "5️⃣ Click, Payme yoki boshqa to'lov tizimlarini ulash mumkinmi?",
        "short": "To'lov tizimlari integratsiyasi",
        "answer": (
            "Albatta! Click, Payme, Uzum Bank to'lov tizimlarini to'g'ridan-to'g'ri bot yoki veb-saytingizga ulab beramiz.\n"
            "Mijozlar to'lov qilganda mablag' to'g'ridan-to'g'ri sizning hisob raqamingizga tushadi va tizim avtomatik chek shakllantiradi."
        ),
    },
]


def format_all_faq_text() -> str:
    """Barcha savol-javoblarni umumiy matn sifatida chiqarish"""
    lines = ["❓ **TEZ-TEZ SO'RALADIGAN SAVOLLAR (FAQ):**\n"]
    for item in FAQ_ITEMS:
        lines.append(f"🔹 **{item['question']}**")
        lines.append(f"{item['answer']}\n")
    lines.append("📞 Boshqa savollaringiz bo'lsa, **'📞 Aloqa'** bo'limi orqali to'g'ridan-to'g'ri bizga yozishingiz mumkin!")
    return "\n".join(lines)
