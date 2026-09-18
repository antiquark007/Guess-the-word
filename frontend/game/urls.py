from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "login/",
        views.login_page,
        name="login"
    ),

    path(
        "register/",
        views.register_page,
        name="register"
    ),

    path(
        "game/",
        views.game_page,
        name="game"
    ),

    path(
        "admin-reports/",
        views.admin_reports,
        name="admin_reports"
    ),
]