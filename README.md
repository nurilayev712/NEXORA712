# ⚡ NEXORA DEV - Dasturchi Portfoli va Xizmatlar Sayti

Ushbu veb-sayt **Telegram botlar** va **zamonaviy veb-saytlar** yaratuvchi dasturchilar uchun maxsus ishlab chiqilgan, yuqori konversiyali va interaktiv portfolio saytidir.

---

## 🌟 Sayt Imkoniyatlari

1. **Zamonaviy Dark Cyber Dizayn**:
   - Tailwind CSS va maxsus neon/glassmorphism effektlari
   - Interaktiv fon (Canvas particle tarmog'i)
   - Hero qismida dinamik yoziluvchi matn effekti (Typing animation)
   - Dasturchi kodli terminal vizualizatsiyasi

2. **Xizmatlar Bo'limi (Services)**:
   - Telegram Botlar (Click/Payme, do'kon, admin panel, WebApp)
   - Veb-saytlar (Landing page, korporativ, e-commerce)
   - CRM & API integratsiyalar (SMS, 1C, ma'lumotlar bazasi)

3. **Interaktiv Narx va Muddat Kalkulyatori (Calculator)**:
   - Mijoz o'ziga kerakli loyiha turi, darajasi va imkoniyatlarini belgilaydi
   - Narx ($ va so'mda) hamda tayyor bo'lish muddati real vaqtda hisoblanadi
   - **"Ushbu hisob bilan buyurtma berish"** tugmasi orqali hisoblangan barcha parametrlar to'g'ridan-to'g'ri sizning Telegramingizga formatlangan matn bo'lib tushadi!

4. **Portfolio & Filter**:
   - Loyihalarni toifalar bo'yicha saralash (Telegram Bot, Veb-sayt, CRM)
   - Har bir loyiha uchun "Batafsil ma'lumot" modal oynasi va texnologiyalar steki

5. **To'g'ridan-to'g'ri Telegram Integratsiyasi**:
   - Tezkor ariza yuborish formasi
   - Doimiy pastda turuvchi suzuvchi (Floating) Telegram tugmasi
   - Barcha arizalar `@NEXORA712` Telegram manziliga to'g'ridan-to'g'ri yo'naltirilgan

---

## 🚀 Saytni Ishga Tushirish

Sayt hech qanday murakkab server talab qilmaydi (toza HTML5, Tailwind CSS, Vanilla JS).

### 1-usul: Oddiy ochish
- `index.html` faylini istalgan brauzerda (Chrome, Edge, Opera) sichqonchaning chap tugmasini 2 marta bosib oching.

### 2-usul: Live Server (Tavsiya etiladi)
- Agar VS Code ishlatayotgan bo'lsangiz, **Live Server** kengaytmasini yoqib `Go Live` tugmasini bosing.
- Yoki PowerShell orqali:
```powershell
# Python orqali mahalliy serverni yoqish
python -m http.server 8000
```
Keyin brauzeringizda `http://localhost:8000` manzilini oching.

---

## 🛠️ Ma'lumotlarni O'zingizga Moslashtirish

1. **Telegram profilingizni o'zgartirish**:
   `index.html` va `script.js` fayllaridagi `@NEXORA712` yoki `https://t.me/NEXORA712` havolasini o'z Telegram username'ingiz bilan almashtirishingiz mumkin.

2. **Yangi loyihalar qo'shish**:
   - `index.html` ichidagi `#projects-grid` bo'limiga yangi karta qo'shing.
   - `script.js` ichidagi `projectDetails` obyektiga yangi loyiha ma'lumotlarini kiriting.

3. **Narxlarni o'zgartirish**:
   `script.js` faylidagi `BASE_PRICES` massivida boshlang'ich narxlarni xohishingizga qarab tahrirlashingiz mumkin.

---

## 🌐 Saytni Internetga Bepul Joylashtirish (Hosting)
Saytni bir necha daqiqada bepul internetga chiqarishingiz mumkin:
- **GitHub Pages**: Fayllarni GitHub repositoriyasiga yuklab, Pages funksiyasini yoqing.
- **Vercel** yoki **Netlify**: Papkani sudrab olib borib tashlang (Drag & Drop), tayyor bepul `.vercel.app` domeni olasiz!
