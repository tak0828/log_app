@echo off
REM ローカル環境でDjangoを実行するスクリプト
cd /d %~dp0
set IS_DOCKER=false
set DJANGO_SETTINGS_MODULE=config.settings
..\venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000

