from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Log
from datetime import date


def login_view(request):
    """ログインページ"""
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "ログインに成功しました")
            return redirect('index')
        else:
            messages.error(request, "ユーザー名またはパスワードが正しくありません")
    
    return render(request, "login.html")


@login_required
def logout_view(request):
    """ログアウト"""
    logout(request)
    messages.success(request, "ログアウトしました")
    return redirect('login')


@login_required
def index(request):
    """フォームなしの簡易投稿（ログイン必須）"""
    if request.method == "POST":
        text = request.POST.get("text", "")
        Log.objects.create(text=text)  # 日時は auto_now_add=True で自動セット
        return redirect("/")

    logs = Log.objects.order_by("-date")
    return render(request, "index.html", {"logs": logs, "user": request.user})