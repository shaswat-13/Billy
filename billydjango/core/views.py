from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
import json

from .forms import SignupForm, LoginForm, IncomeForm, ExpenseForm
from .models import Income, Expense

# ============================================
# AUTH & UTILITY VIEWS
# ============================================

def index(request):
    """Landing page view"""
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    return render(request, 'core/index.html')

def check_auth(request):
    """Essential for React to check if session is valid and get CSRF token"""
    get_token(request) 
    if request.user.is_authenticated:
        return JsonResponse({
            'isAuthenticated': True,
            'user': {
                'username': request.user.username,
                'first_name': request.user.first_name,
            }
        })
    return JsonResponse({'isAuthenticated': False}, status=401)

@csrf_exempt
@require_http_methods(["POST"])
def signup_view(request):
    try:
        data = json.loads(request.body)
        username = data.get('username', '').strip()
        password = data.get('password', '')
        email = data.get('email', '').strip()
        name = data.get('name', '').strip()

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already taken'}, status=400)

        name_parts = name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''

        user = User.objects.create_user(
            username=username, email=email, password=password,
            first_name=first_name, last_name=last_name
        )
        login(request, user)
        return JsonResponse({'success': True, 'user': {'username': user.username}})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            return JsonResponse({'success': True, 'user': {'username': user.username}})
        return JsonResponse({'error': 'Invalid credentials'}, status=401)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({'success': True})

# ============================================
# DATA VIEWS (API)
# ============================================

@login_required
def dashboard_api(request):
    """The main data source for your React Dashboard"""
    incomes = Income.objects.filter(user=request.user).order_by('-date')
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    
    total_inc = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
    total_exp = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    return JsonResponse({
        'incomes': [{'id': i.id, 'amount': str(i.amount), 'source': i.source, 'date': i.date.strftime('%Y-%m-%d')} for i in incomes],
        'expenses': [{'id': e.id, 'amount': str(e.amount), 'description': e.description, 'date': e.date.strftime('%Y-%m-%d')} for e in expenses],
        'total_income': float(total_inc),
        'total_expenses': float(total_exp),
        'balance': float(total_inc - total_exp),
        'user': {'username': request.user.username, 'first_name': request.user.first_name}
    })

@csrf_exempt
@login_required
@require_http_methods(["POST"])
def add_income(request):
    try:
        data = json.loads(request.body)
        income = Income.objects.create(
            user=request.user,
            amount=data.get('amount'),
            source=data.get('source'),
            date=data.get('date')
        )
        return JsonResponse({'success': True, 'id': income.id}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@login_required
@require_http_methods(["POST"])
def add_expense(request):
    try:
        data = json.loads(request.body)
        expense = Expense.objects.create(
            user=request.user,
            amount=data.get('amount'),
            description=data.get('description'),
            date=data.get('date')
        )
        return JsonResponse({'success': True, 'id': expense.id}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@login_required
def delete_income(request, income_id):
    income = get_object_or_404(Income, id=income_id, user=request.user)
    income.delete()
    return JsonResponse({'success': True})

@csrf_exempt
@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    expense.delete()
    return JsonResponse({'success': True})