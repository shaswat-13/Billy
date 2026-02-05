from django.db import models
from django.contrib.auth.models import User


class Income(models.Model):
    """
    Income Model - Represents a single income record
    
    Each income belongs to exactly ONE user.
    If user is deleted, their incomes are deleted too (CASCADE).
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='incomes'
    )
    
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    
    source = models.CharField(
        max_length=100,
        help_text="e.g., Salary, Freelance, Gift"
    )
    
    date = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        # Show newest incomes first
        verbose_name = 'Income'
        verbose_name_plural = 'Incomes'
    
    def __str__(self):
        return f"{self.source} - ${self.amount} ({self.date})"
        # Shows: "Salary - $5000.00 (2026-02-01)" in admin


class Expense(models.Model):
    """
    Expense Model - Represents a single expense record
    
    Each expense belongs to exactly ONE user.
    Parallel structure to Income for symmetry.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='expenses'
    )
    
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    
    description = models.CharField(
        max_length=200,
        help_text="What did you buy?"
    )
    
    date = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    # When was this record created in the system?
    
    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'
    
    def __str__(self):
        return f"{self.description} - ${self.amount} ({self.date})"
        # Shows: "Groceries - $150.00 (2026-02-05)" in admin


