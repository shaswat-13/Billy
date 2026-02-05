from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignupForm, LoginForm

def index(request):
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
    # This code only runs if user is authenticated
    # request.user is guaranteed to be a real User object (not AnonymousUser)
    return render(request, 'core/dashboard.html', {
    'user': request.user
    })