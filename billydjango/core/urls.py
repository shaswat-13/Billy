from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    # Public routes
    path("", views.index, name="landing"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    
    # Protected routes
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    
    # Income CRUD
    path("income/add/", views.add_income, name="add_income"),
    path("income/delete/<int:income_id>/", views.delete_income, name="delete_income"),
    
    # Expense CRUD
    path("expense/add/", views.add_expense, name="add_expense"),
    path("expense/delete/<int:expense_id>/", views.delete_expense, name="delete_expense"),
]