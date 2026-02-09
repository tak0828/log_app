from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.http import HttpResponse
from .models import Log, CustomUser
import csv


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
    sort = request.GET.get("sort", "desc")
    order_by = "-date" if sort != "asc" else "date"

    if request.method == "POST":
        text = request.POST.get("text", "")
        Log.objects.create(
            user=request.user,
            text=text,
        )
        return redirect("/")

    logs = Log.objects.filter(user=request.user).order_by(order_by)
    return render(
        request,
        "index.html",
        {"logs": logs, "user": request.user, "sort": sort},
    )


@login_required
def activity_view(request):
    """Activity trend page."""
    activity = (
        Log.objects.filter(user=request.user)
        .annotate(day=TruncDate("date"))
        .values("day")
        .annotate(count=Count("id"))
        .order_by("day")
    )
    return render(
        request,
        "activity.html",
        {"activity": activity, "user": request.user},
    )


@login_required
def csv_view(request):
    """CSV download page."""
    return render(request, "csv.html", {"user": request.user})


@login_required
def csv_download(request):
    """CSV download endpoint."""
    logs = Log.objects.filter(user=request.user).order_by("-date")

    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="logs.csv"'

    response.write("\ufeff")
    writer = csv.writer(response)
    writer.writerow(["日時", "内容"])
    for log in logs:
        writer.writerow([log.date.strftime("%Y-%m-%d %H:%M:%S"), log.text])

    return response
