@echo off
chcp 65001 >nul
title NEXORA712 - Avtomatik Yangilash (GitHub & Render)
echo ========================================================
echo   NEXORA712 - SAYT VA BOTNI 1-KLIKDA YANGILASH
echo ========================================================
echo.
echo [1/3] Barcha o'zgarishlar yig'ilmoqda (git add)...
git add .

echo.
set /p msg="Kiritilgan o'zgarish haqida qisqa izoh (yoki Enter bosing): "
if "%msg%"=="" set msg=Sayt va bot kodlari yangilandi

echo [2/3] Kommit qilinmoqda...
git commit -m "%msg%"

echo.
echo [3/3] GitHub va Renderga yuborilmoqda (git push)...
git push origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================================
    echo  [MUVAFFAQIYATLI] Kodlar GitHub ga yuklandi!
    echo.
    echo  🚀 RENDER AVTOMATIK ISHGA TUSHDI (Auto-Deploy):
    echo  Render 1-2 daqiqa ichida yangi kodlarni o'rnatib,
    echo  Web sayt, Instagram Bio va Telegram Botni uzluksiz
    echo  yangi versiyaga o'tkazadi!
    echo ========================================================
) else (
    echo.
    echo [XATOLIK] Kodlarni yuklashda muammo yuz berdi.
)
echo.
pause
