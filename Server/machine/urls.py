from django.urls import path
from . import views

urlpatterns = [
    path("login", views.login_user),
    path("logout", views.logout_user),
    path("register", views.register_user),
    path("test", views.test),

    path("", views.get_rules),
    path("addMoney", views.add_money),
    path("roll", views.spin_machine),
    path("history", views.get_user_history),
    path("history/<int:pk>", views.get_user_roll),
    path("statistics", views.get_user_statistics),
]
