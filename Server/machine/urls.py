from django.urls import path
from . import views

urlpatterns = [
    path("login", views.login_user, name="login"),
    path("logout", views.logout_user),
    path("register", views.register_user),
    path("user", views.user_info, name="user"),

    path("", views.get_rules, name="rules"),
    path("addMoney", views.add_money, name="addMoney"),
    path("roll", views.spin_machine, name="roll"),
    path("history", views.get_user_history, name="rollHistory"),
    path("history/<int:pk>", views.get_user_roll, name="userHistory"),
    path("statistics", views.get_user_statistics, name="statistics"),
    path("leaderboard/<str:criteria>", views.get_leaderboard, name="leaderboard"),
]
