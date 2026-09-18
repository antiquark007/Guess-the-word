from django.shortcuts import render
from django.shortcuts import redirect


def home(request):

    return render(
        request,
        "game/home.html"
    )


def login_page(request):

    return render(
        request,
        "game/login.html"
    )


def register_page(request):

    return render(
        request,
        "game/register.html"
    )


def game_page(request):

    return render(
        request,
        "game/game.html"
    )


def admin_reports(request):

    return render(
        request,
        "game/admin_reports.html"
    )