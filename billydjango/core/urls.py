from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.index, name="landing"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_view, name="dashboard")
]