@echo off
title NEXORA DEV - Telegram Bot
chcp 65001 > nul
echo ======================================================
echo           ⚡ NEXORA DEV TELEGRAM BOT ⚡
echo ======================================================
echo.

python run_bot.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Botni ishga tushirishda xatolik yuz berdi.
    echo Iltimos, 'bot\.env' faylida BOT_TOKEN to'g'ri kiritilganligini tekshiring!
    pause
)
