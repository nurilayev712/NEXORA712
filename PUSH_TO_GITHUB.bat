@echo off
chcp 65001 >nul
title NEXORA712 - GitHub ga Yuklash
echo ========================================================
echo       NEXORA712 - GITHUB GA AVTOMATIK YUKLASH
echo ========================================================
echo.
echo [1/2] Git masofaviy ombori (remote) sozlanmoqda...
git branch -M main
git remote remove origin 2>nul
git remote add origin https://github.com/nurilayev712/NEXORA712.git

echo [2/2] Barcha papkalar va fayllar GitHub ga yuklanmoqda...
echo Iltimos, kuting...
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================================
    echo  [MUVAFFAQIYATLI] Barcha papkalar va kodlar GitHub ga yuklandi!
    echo  Havola: https://github.com/nurilayev/nexora712
    echo ========================================================
) else (
    echo.
    echo ========================================================
    echo  [OGOHLANTIRISH] Agar repo topilmadi desa:
    echo  1. Brauzeringizda https://github.com/new manzilini oching
    echo  2. Repository name ga 'nexora712' deb yozing
    echo  3. 'Create repository' tugmasini bosing
    echo  4. Keyin ushbu faylni qaytadan ishga tushiring!
    echo ========================================================
)
echo.
pause
