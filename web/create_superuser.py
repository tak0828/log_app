#!/usr/bin/env python
"""スーパーユーザーを作成するスクリプト"""
import os
import sys
import django

# Djangoの設定を読み込む
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from app.models import CustomUser

# スーパーユーザーが既に存在するか確認
if CustomUser.objects.filter(is_superuser=True).exists():
    print("スーパーユーザーは既に存在します。")
    sys.exit(0)

# スーパーユーザーを作成
username = 'admin'
email = 'admin@example.com'
password = 'admin123'

if CustomUser.objects.filter(username=username).exists():
    print(f"ユーザー '{username}' は既に存在します。")
else:
    CustomUser.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print(f"スーパーユーザー '{username}' を作成しました。")
    print(f"ユーザー名: {username}")
    print(f"パスワード: {password}")
    print("\n※本番環境では必ずパスワードを変更してください！")


