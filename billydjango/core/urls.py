from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.index, name="landing"),
    path("api/check-auth/", views.check_auth, name="check-auth"),
    path("api/dashboard/", views.dashboard_api, name="dashboard-api"), # Updated
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("income/add/", views.add_income, name="add-income"),
    path("expense/add/", views.add_expense, name="add-expense"),
    path("income/delete/<int:income_id>/", views.delete_income, name="delete-income"),
    path("expense/delete/<int:expense_id>/", views.delete_expense, name="delete-expense"),
]