from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_rules),
    path("login", views.login_user),
    path("logout", views.logout_user),
    path("register", views.register_user),
    path("test", views.test),
    path("roll", views.spin_machine),
]
