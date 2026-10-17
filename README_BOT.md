# ⚡ NEXORA DEV - Professional Telegram Bot (aiogram 3.x)

Ushbu bot **Telegram botlar** va **zamonaviy veb-saytlar** buyurtma qilish, narxlar bilan tanishish, portfolioni ko'rish va admin tomonidan arizalarni qulay boshqarish uchun ishlab chiqilgan to'liq asinxron va productionga tayyor Telegram botidir.

---

## 🛠️ Ishlatilgan Texnologiyalar

- **Til:** Python 3.10+
- **Freymvork:** [aiogram 3.x](https://docs.aiogram.dev/) (zamonaviy asinxron Telegram freymvorki)
- **Ma'lumotlar bazasi:** SQLite + [aiosqlite](https://github.com/omnilib/aiosqlite) (to'liq asinxron va xavfsiz)
- **Konfiguratsiya:** `python-dotenv` (.env orqali xavfsiz boshqaruv)
- **Holatlar boshqaruvi:** FSM (Finite State Machine)

---

## 📁 Loyiha Strukturasi

```text
NEXORA712/
├── bot/
│   ├── data/
│   │   ├── __init__.py
│   │   ├── prices.py             # Xizmatlar va narxlar (oson tahrirlanadigan)
│   │   └── faq.py                # Tez-tez so'raladigan savol-javoblar
│   ├── database/
│   │   ├── __init__.py
│   │   ├── db.py                 # SQLite CRUD, buyurtmalar, statistika va foydalanuvchilar
│   │   └── bot.db                # SQLite ma'lumotlar bazasi (avtomatik yaratiladi)
│   ├── filters/
│   │   ├── __init__.py
│   │   └── admin_filter.py       # Admin huquqini tekshiruvchi filtr
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── start.py              # /start, /help va bekor qilish
│   │   ├── order.py              # Bosqichma-bosqich buyurtma berish FSM
│   │   ├── sections.py           # Narxlar, Portfolio, FAQ va Aloqa bo'limlari
│   │   └── admin.py              # Admin panel: /admin, /orders, /stats, /broadcast
│   ├── keyboards/
│   │   ├── __init__.py
│   │   ├── reply.py              # Asosiy menyu, kontakt yuborish, bekor qilish
│   │   ├── inline.py             # Byudjet, muddat, tasdiqlash, bo'limlar navigatsiyasi
│   │   └── admin_kb.py           # Admin buyurtma boshqaruvi, statuslar, broadcast
│   ├── states/
│   │   ├── __init__.py
│   │   ├── order_state.py        # Buyurtma berish FSM holatlari
│   │   └── admin_state.py        # Broadcast va yangi portfolio FSM holatlari
│   ├── utils/
│   │   ├── __init__.py
│   │   └── formatters.py         # Chiroyli formatlangan hisobotlar va bildirishnomalar
│   ├── .env.example              # Namuna konfiguratsiya fayli
│   ├── .env                      # Shaxsiy sozlamalar (Token, Admin ID)
│   ├── config.py                 # Konfiguratsiya yuklovchi
│   ├── main.py                   # Botni asosiy ishga tushiruvchi modul
│   └── requirements.txt          # Python kutubxonalari ro'yxati
├── run_bot.bat                   # Windows uchun 1-klikda ishga tushiruvchi fayl
├── run_bot.py                    # Ildizdagi qulay ishga tushirish skripti
└── README_BOT.md                 # Bot qo'llanmasi
```

---

## 🚀 O'rnatish va Sozlash

### 1-qadam: Bot Token va Admin ID olish

1. Telegramda [@BotFather](https://t.me/BotFather) ga kiring va `/newbot` buyrug'i orqali yangi bot ochib, **API Token** oling.
2. O'zingizning Telegram ID raqamingizni bilish uchun [@userinfobot](https://t.me/userinfobot) ga kiring.

### 2-qadam: `.env` Faylini Sozlash

`bot/.env` faylini oching va ma'lumotlaringizni kiriting:

```env
# Telegram Bot Token (@BotFather dan olingan)
BOT_TOKEN=123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ_example

# Sizning Telegram ID raqamingiz (bitta yoki vergul bilan: 123456789,987654321)
ADMIN_ID=123456789

# Telegram profilingiz username'i (@ belgisiz)
ADMIN_USERNAME=NEXORA712

# Bog'lanish uchun telefon raqami
ADMIN_PHONE=+998901234567
```

### 3-qadam: Kutubxonalarni O'rnatish

Konsolda quyidagi buyruqni bajaring:

```bash
pip install -r bot/requirements.txt
```

---

## ⚡ Botni Ishga Tushirish

### Windows tizimida (Eng oson usul):
Shunchaki loyiha papkasidagi **`run_bot.bat`** faylini ikki marta bosing!

### Terminal / Konsol orqali:
```bash
python run_bot.py
# yoki
python -m bot.main
```

---

## 📱 Bot Imkoniyatlari va Foydalanish

### 1. Asosiy Menyu (`/start`)
- **🤖 Telegram bot buyurtma qilish** — Bot ishlab chiqish uchun ariza qoldirish.
- **🌐 Veb-sayt buyurtma qilish** — Sayt ishlab chiqish uchun ariza qoldirish.
- **💰 Narxlar** — Bot va veb-sayt narxlari, imkoniyatlari bilan batafsil tanishish.
- **📁 Portfolio** — Bajarilgan ishlar ro'yxati, toifalar bo'yicha saralash.
- **❓ Savol-javob** — Ko'p beriladigan savollarga tezkor javoblar (FAQ).
- **📞 Aloqa** — Admin bilan to'g'ridan-to'g'ri bog'lanish va qo'ng'iroq qilish.

### 2. Buyurtma Berish Jarayoni (FSM)
1. **Xizmat turi** tanlangan tugmaga ko'ra avtomatik belgilanadi.
2. **Loyiha nomi / g'oyasi** so'raladi.
3. **Loyiha haqida batafsil tavsif** so'raladi.
4. **Taxminiy byudjet** so'raladi ($50-100, $100-300, $300-500, $500+ yoki o'zi yozishi mumkin).
5. **Bajarilish muddati** so'raladi (1-3 kun, 3-7 kun, 1-2 hafta, 1 oy+).
6. **Aloqa ma'lumoti** so'raladi (Telegram kontakt yuborish tugmasi yoki matn shaklida).
7. **Xulosa va tasdiqlash**: Barcha ma'lumotlar jamlanib, mijozdan tasdiq olinadi.
8. **Tasdiqlangach**:
   - Mijozga buyurtma ID raqami beriladi.
   - Adminga darhol to'liq buyurtma tafsilotlari va `✅ Qabul qilish` / `❌ Rad etish` tugmalari bilan yetkaziladi.

---

## 👑 Admin Panel Funksiyalari (Faqat ADMIN_ID uchun)

Admin paneli faqat `.env` da ko'rsatilgan admin ID foydalanuvchilariga ko'rinadi:

- **/admin** — Asosiy admin boshqaruv paneli menyusi.
- **/orders** — Buyurtmalar ro'yxati va holatlar bo'yicha filtrlar:
  - 🆕 Yangi buyurtmalar (`pending`)
  - ⏳ Jarayondagi buyurtmalar (`in_progress`)
  - ✅ Bajarilgan buyurtmalar (`completed`)
  - ❌ Bekor qilingan / Rad etilgan (`rejected`)
  - 📋 Barcha buyurtmalar
  - Har bir buyurtma holatini bitta tugma bilan o'zgartirish mumkin. Holat o'zgarganda mijozga avtomatik bildirishnoma boradi!
- **/stats** — To'liq statistik hisobot:
  - Jami foydalanuvchilar soni
  - Jami arizalar soni
  - Bugungi va shu oylik buyurtmalar
  - Bot va sayt arizalari nisbati (soni va foizda)
  - Holatlar taqsimoti
- **/broadcast** — Barcha foydalanuvchilarga xabar tarqatish:
  - Matn, rasm yoki video xabar yuborish
  - Yuborishdan oldin ko'rib chiqish (preview) va tasdiqlash
  - Flood-limitlarni hisobga olgan xavfsiz yuborish va yakuniy hisobot
- **Portfolio qo'shish** — Bot orqali yangi portfolio loyihasini bazaga qo'shish.

---

## 🌐 Serverda (VPS / Linux) 24/7 Ishga Tushirish

Botni serverda doimiy o'chmasdan ishlashi uchun **systemd** xizmatini sozlash:

1. Serverga fayllarni yuklang va virtual muhit yarating:
```bash
cd /root/NEXORA712
python3 -m venv venv
source venv/bin/activate
pip install -r bot/requirements.txt
```

2. Systemd servisini yarating:
```bash
sudo nano /etc/systemd/system/nexorabot.service
```

Quyidagi matnni joylang:
```ini
[Unit]
Description=NEXORA DEV Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/NEXORA712
ExecStart=/root/NEXORA712/venv/bin/python run_bot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

3. Xizmatni yoqing:
```bash
sudo systemctl daemon-reload
sudo systemctl enable nexorabot
sudo systemctl start nexorabot
sudo systemctl status nexorabot
```
