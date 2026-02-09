# ローカル環境でDjangoを実行するPowerShellスクリプト
$env:IS_DOCKER = "false"
$env:DJANGO_SETTINGS_MODULE = "config.settings"
Set-Location $PSScriptRoot
..\venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000

