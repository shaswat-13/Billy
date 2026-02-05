from django.contrib import admin
from .models import Income, Expense


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    """
    Customize how Income appears in Django admin
    """
    list_display = ['source', 'amount', 'date', 'user', 'created_at']
    # Columns shown in the list view
    
    list_filter = ['date', 'user', 'source']
    # Sidebar filters for easy searching
    
    search_fields = ['source', 'user__username']
    # Search by source or username
    
    date_hierarchy = 'date'
    # Date navigation at the top
    
    ordering = ['-date', '-created_at']
    # Show newest first
    
    readonly_fields = ['created_at']
    # Can't edit system timestamp


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    """
    Customize how Expense appears in Django admin
    """
    list_display = ['description', 'amount', 'date', 'user', 'created_at']
    
    list_filter = ['date', 'user']
    
    search_fields = ['description', 'user__username']
    
    date_hierarchy = 'date'
    
    ordering = ['-date', '-created_at']
    
    readonly_fields = ['created_at']


"""
WHAT THIS DOES:

1. @admin.register(Income):
   - Makes Income model visible in /admin/
   - Applies custom configuration

2. list_display:
   - Columns shown in the admin list
   - Makes scanning records easier

3. list_filter:
   - Sidebar filters
   - Filter by date, user, etc.

4. search_fields:
   - Search box at the top
   - Search by source/description or username

5. date_hierarchy:
   - Date navigation breadcrumbs
   - Click year → month → day

6. readonly_fields:
   - Can't edit created_at (it's auto-generated)

This makes admin MUCH more usable for testing.
"""