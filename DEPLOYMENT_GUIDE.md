# 🚀 NEXORA712 - GitHub va Render 24/7 Joylash Qo'llanmasi

Ushbu qo'llanma orqali loyihangizdagi:
- 🌐 **Google / Web sayt** (`index.html`)
- 📱 **Instagram Bio havolalar sahifasi** (`bio.html`)
- ⚡ **Telegram WebApp ilovasi** (`webapp/index.html`)
- 🤖 **Aiogram 3 Telegram Bot** (`bot/`)

barchasini bitta **Render Web Service** orqali **24/7 mutlaqo bepul va uxlamaydigan (spin-down bo'lmaydigan)** qilib ishga tushirasiz.

---

## 1-QADAM: GitHub ga Yuklash

Loyiha kompyuteringizda allaqachon Git orqali kommit qilindi (`main` tarmog'ida).
Endi uni GitHub akkauntingizga yuklaysiz:

1. [GitHub.com](https://github.com) ga kiring va **New Repository** (Yangi repozitoriy) tugmasini bosing.
2. Repozitoriy nomini yozing (masalan: `nexora712` yoki `nexora-platform`).
3. Uni **Public** qilib qoldiring (Render bepul tarifida Public bilan juda qulay ulanadi).
4. Hech qanday README yoki .gitignore qo'shmang (bizda allaqachon mukammal tayyorlangan).
5. **Create repository** tugmasini bosing.
6. Kompyuteringizdagi PowerShell terminalida quyidagi 2 ta buyruqni bering (o'zingizning GitHub username va repo nomingizni qo'ying):

```powershell
git remote add origin https://github.com/nurilayev/nexora712.git
git push -u origin main
```

*(Agar parol so'rasa, GitHub Personal Access Token (PAT) yoki brauzer orqali ruxsat berish kifoya).*

---

## 2-QADAM: Render.com da 24/7 Ishga Tushirish

Render loyihangizdagi `render.yaml` va `server.py` fayllarini avtomatik taniydi.

### A usuli: Blueprint (Eng oson 1-klik usuli)
1. [Render.com](https://render.com) ga kiring va GitHub orqali kiring.
2. Yuqori o'ng burchakdagi **New +** tugmasini bosing va **Blueprint** ni tanlang.
3. Yangi ochilgan GitHub repozitoriyangizni (`nexora712`) tanlang va **Connect** qiling.
4. Render loyihangizdagi `render.yaml` faylini o'qiydi. Sizdan faqat muhit o'zgaruvchilarini so'raydi:
   - `BOT_TOKEN`: @BotFather bergan tokeningiz
   - `ADMIN_ID`: Sizning Telegram ID raqamingiz (`5882864189`)
   - `ADMIN_USERNAME`: `NEXORA712`
   - `ADMIN_PHONE`: `+998901234567`
5. **Apply** tugmasini bosing! 3-4 daqiqada server to'liq ko'tariladi.

### B usuli: Qo'lda Web Service ochish
1. **New +** -> **Web Service** ni tanlang.
2. Repozitoriyangizni tanlang.
3. Sozlamalar:
   - **Name**: `nexora712`
   - **Language**: `Python 3`
   - **Region**: `Frankfurt (EU Central)`
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python server.py`
   - **Plan**: `Free`
4. **Environment Variables** (Muhit o'zgaruvchilari) bo'limida qo'shing:
   - `BOT_TOKEN` = Sizning bot tokeningiz
   - `ADMIN_ID` = `5882864189`
   - `ADMIN_USERNAME` = `NEXORA712`
   - `ADMIN_PHONE` = `+998901234567`
   - `PYTHON_VERSION` = `3.11.9`
5. **Create Web Service** tugmasini bosing.

---

## 3-QADAM: Render Serverini 24/7 Uxlab Qolmasligini Ta'minlash

> [!IMPORTANT]
> Render Free tarifi har 15 daqiqada so'rov kelmasa uxlaydi (spin-down).
> Buning oldini olish va bot 24/7 sekundiga javob berishi uchun quyidagi bepul monitoringni yoqamiz:

### 🌟 UptimeRobot orqali (Tavsiya etiladi - 100% Bepul)
1. [UptimeRobot.com](https://uptimerobot.com) saytiga kiring (bepul ro'yxatdan o'ting).
2. **Add New Monitor** tugmasini bosing:
   - **Monitor Type**: `HTTP(s)`
   - **Friendly Name**: `NEXORA 24/7 Keeper`
   - **URL (or IP)**: `https://sizning-app.onrender.com/health`
   - **Monitoring Interval**: `5 minutes` (har 5 daqiqada)
3. **Create Monitor** tugmasini bosing!

✅ **Natija:** UptimeRobot har 5 daqiqada sizning serveringizdagi `/health` manziliga signal yuboradi. Render serveringiz **HECH QACHON UXLAMAYDI** va Telegram botingiz 24/7 faol turadi!

---

## 4-QADAM: Tayyor Manzillardan Foydalanish

Render sizga bepul HTTPS domen beradi (masalan: `https://nexora712.onrender.com`).

Ushbu bitta domen orqali sizda hammasi ishlaydi:
1. 🌐 **Google / Web saytingiz**: `https://nexora712.onrender.com/`
2. 📱 **Instagram Bio sahifangiz**: `https://nexora712.onrender.com/bio`
3. ⚡ **Telegram WebApp**: `https://nexora712.onrender.com/webapp`
4. 💓 **Uptime Monitoring**: `https://nexora712.onrender.com/health`
5. 🤖 **Telegram Bot**: Fondan uzluksiz xabarlarni qabul qilib, javob beradi.

---

## 5-QADAM: Telegram Botdagi WebApp Menyu Tugmasini Yangilash

Render domeningiz chiqqandan so'ng (masalan: `https://nexora712.onrender.com`), Telegramdagi "NEXORA WebApp" tugmasi shu yangi manzilni ochishi uchun:

1. Render Environment bo'limida `WEBAPP_URL` qiymatini `https://nexora712.onrender.com/webapp` ga o'zgartiring.
2. Yoki BotFather orqali:
   - `@BotFather` ga kiring -> `/mybots` -> Botingizni tanlang -> **Bot Settings** -> **Menu Button** -> **Configure menu button** -> Havolaga `https://nexora712.onrender.com/webapp` manzilini kiriting.

Tabriklaymiz! Sizning to'liq ekotizimingiz professional darajada 24/7 ishga tushdi! 🎉
