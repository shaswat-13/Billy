from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from datetime import date
from .models import Income, Expense


class SignupForm(forms.Form):
    name = forms.CharField(
        label="Full name",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your full name'
        })
    )

    username = forms.CharField(
        label="Username",
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username'
        })
    )
    
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter a strong password'
        })
    )

    confirm_password = forms.CharField(
    label="Confirm Password",
    widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Re-enter your password'
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already registered.")
        return email
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        # validation using built-in password validators
        validate_password(password)
        return password
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username or Email",
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username or email'
        })
    )
    
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )
    
    remember_me = forms.BooleanField(
        label="Remember me",
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        if username and password:
            # Try to authenticate with username first
            user = authenticate(username=username, password=password)
            
            # If authentication fails, try with email
            if user is None:
                try:
                    user_obj = User.objects.get(email=username)
                    user = authenticate(username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass
            
            # If still no user, raise validation error
            if user is None:
                raise ValidationError("Invalid username/email or password.")
            
            # If user is inactive
            if not user.is_active:
                raise ValidationError("This account is inactive.")
            
            # Store the authenticated user for easy access in the view
            cleaned_data['user'] = user
        
        return cleaned_data


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'source', 'date']
        # IMPORTANT: 'user' is NOT in fields - we set it in the view
        
        widgets = {
            'amount': forms.NumberInput(attrs={
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0.01'
            }),
            'source': forms.TextInput(attrs={
                'placeholder': 'e.g., Salary, Freelance, Gift'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date'
            })
        }
        
        labels = {
            'amount': 'Amount ($)',
            'source': 'Income Source',
            'date': 'Date'
        }
    
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        
        if amount is not None and amount <= 0:
            raise ValidationError("Amount must be greater than zero.")
        
        return amount
    
    def clean_date(self):
        income_date = self.cleaned_data.get('date')
        
        if income_date and income_date > date.today():
            raise ValidationError("Income date cannot be in the future.")
        
        return income_date


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'description', 'date']
        
        widgets = {
            'amount': forms.NumberInput(attrs={
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0.01'
            }),
            'description': forms.TextInput(attrs={
                'placeholder': 'e.g., Groceries, Rent, Entertainment'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date'
            })
        }
        
        labels = {
            'amount': 'Amount ($)',
            'description': 'What did you buy?',
            'date': 'Date'
        }
    
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        
        if amount is not None and amount <= 0:
            raise ValidationError("Amount must be greater than zero.")
        
        return amount
    
    def clean_date(self):
        expense_date = self.cleaned_data.get('date')
        
        if expense_date and expense_date > date.today():
            raise ValidationError("Expense date cannot be in the future.")
        
        return expense_date