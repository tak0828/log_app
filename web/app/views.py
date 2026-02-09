from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Log, CustomUser


def login_view(request):
    """Login page."""
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "ログインしました。")
            return redirect('index')
        messages.error(request, "無効なユーザー名またはパスワードです。")

    return render(request, "login.html")


def signup_view(request):
    """Signup page."""
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        password_confirm = request.POST.get("password_confirm", "")

        if not username or not email or not password:
            messages.error(request, "必須項目をすべて入力してください。")
            return render(request, "signup.html")

        if password != password_confirm:
            messages.error(request, "パスワードが一致しません。")
            return render(request, "signup.html")

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "そのユーザー名はすでに使用されています。")
            return render(request, "signup.html")

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "そのメールアドレスはすでに登録されています。")
            return render(request, "signup.html")

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        login(request, user)
        messages.success(request, "アカウントが作成されました。")
        return redirect('index')

    return render(request, "signup.html")


@login_required
def logout_view(request):
    """Logout."""
    logout(request)
    messages.success(request, "ログアウトしました。")
    return redirect('login')


@login_required
def index(request):
    """Log list and create."""
    if request.method == "POST":
        text = request.POST.get("text", "")
        Log.objects.create(
            user=request.user,
            text=text,
        )
        return redirect("/")

    logs = Log.objects.filter(user=request.user).order_by("-date")
    return render(request, "index.html", {"logs": logs, "user": request.user})
