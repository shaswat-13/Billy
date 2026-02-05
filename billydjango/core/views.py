from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .forms import SignupForm, LoginForm, IncomeForm, ExpenseForm
from .models import Income, Expense

def index(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    
    return render(request, 'core/index.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        
        if form.is_valid():
            # Extract cleaned data
            name = form.cleaned_data['name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Split name into first_name and last_name
            name_parts = name.split(' ', 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ''
            
            # Create user using Django's user manager
            user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )

            
            # Log the user in immediately after signup
            login(request, user)
            
            # Success message
            messages.success(request, f'Welcome, {first_name}! Your account has been created.')
            
            # Redirect to dashboard (prevents form resubmission)
            return redirect('core:dashboard')  # Change 'dashboard' to your actual URL name
    
    else:
        # GET request - show empty form
        form = SignupForm()
    
    return render(request, 'core/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            # Fetch the authenticated user from cleaned_data
            user = form.cleaned_data['user']
            
            # Create session and log user in
            login(request, user)
            
            # Handle "remember me" functionality
            remember_me = form.cleaned_data.get('remember_me')
            if not remember_me:
                # Session expires when browser closes
                request.session.set_expiry(0)
            else:
                # Session persists for 2 weeks (default Django behavior)
                request.session.set_expiry(1209600)
            
            # Success message
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            
            # Redirect to dashboard (or to 'next' parameter if it exists)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('core:dashboard')  
    else:
        # GET request - show empty form
        form = LoginForm()
    
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('core:landing')  

@login_required
def dashboard_view(request):
    # Fetch ONLY the logged-in user's records
    incomes = Income.objects.filter(user=request.user).order_by('-date')
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    
    # more efficient to aggegrate and sum in db than in Python
    total_income = Income.objects.filter(user=request.user).aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    total_expenses = Expense.objects.filter(user=request.user).aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    # SAVINGS CALCULATION - Computed on server
    balance = total_income - total_expenses
    
    return render(request, 'core/dashboard.html', {
        'user': request.user,
        'incomes': incomes,
        'expenses': expenses,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'balance': balance,
    })

@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        
        if form.is_valid():
            # Create income object but DON'T save to database yet
            income = form.save(commit=False)
            
            # Set ownership
            income.user = request.user
            
            # NOW save to database
            income.save()
            
            messages.success(request, f'Income of ${income.amount} added successfully!')
            return redirect('core:dashboard')
    
    else:
        # GET request - show empty form
        form = IncomeForm()
    
    return render(request, 'core/add_income.html', {'form': form})


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        
        if form.is_valid():
            # Create expense object but DON'T save yet
            expense = form.save(commit=False)
            
            # Set ownership
            expense.user = request.user
            
            # Save to database
            expense.save()
            
            messages.success(request, f'Expense of ${expense.amount} added successfully!')
            return redirect('core:dashboard')
    
    else:
        # GET request - show empty form
        form = ExpenseForm()
    
    return render(request, 'core/add_expense.html', {'form': form})

@login_required
def delete_income(request, income_id):
    income = get_object_or_404(Income, id=income_id, user=request.user)
    
    # Only runs if ownership verified
    income.delete()
    
    messages.success(request, 'Income deleted successfully!')
    return redirect('core:dashboard')


@login_required
def delete_expense(request, expense_id):
    # Ownership check built into this line
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    
    expense.delete()
    
    messages.success(request, 'Expense deleted successfully!')
    return redirect('core:dashboard')