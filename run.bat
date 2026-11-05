@echo off
chcp 65001 >nul
title Kokoro-82M TTS Local WebUI

echo กำลังเปิดใช้งาน Virtual Environment...
call venv\Scripts\activate

echo กำลังรันแอปพลิเคชัน Kokoro WebUI...
python app.py

pause