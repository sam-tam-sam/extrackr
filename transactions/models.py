from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone


class Category(models.Model):
    CATEGORY_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    name = models.CharField(max_length=100)
    category_type = models.CharField(max_length=10, choices=CATEGORY_TYPES)
    icon = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=7, default='#3B82F6')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_category_type_display()})"


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    description = models.TextField(blank=True, null=True)
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'transactions'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.get_transaction_type_display()}: {self.amount} - {self.category.name}"

    @property
    def is_income(self):
        return self.transaction_type == 'income'

    @property
    def is_expense(self):
        return self.transaction_type == 'expense'


class RecurringTransaction(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recurring_transactions')
    transaction_type = models.CharField(max_length=10, choices=Transaction.TRANSACTION_TYPES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='recurring_transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    description = models.TextField(blank=True, null=True)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)
    next_occurrence = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'recurring_transactions'
        ordering = ['next_occurrence']

    def __str__(self):
        return f"Recurring {self.get_transaction_type_display()}: {self.amount} - {self.category.name}"

    def save(self, *args, **kwargs):
        if not self.next_occurrence:
            self.next_occurrence = self.start_date
        super().save(*args, **kwargs)


class Budget(models.Model):
    PERIOD_CHOICES = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='budgets')
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES, default='monthly')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'budgets'
        unique_together = ['user', 'category', 'period', 'start_date']
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.category.name} Budget: {self.amount} ({self.get_period_display()})"

    def get_spent_amount(self):
        """Calculate amount spent for this budget period"""
        from django.db.models import Sum
        
        if self.period == 'monthly':
            start_date = self.start_date.replace(day=1)
            if self.start_date.month == 12:
                end_date = self.start_date.replace(year=self.start_date.year + 1, month=1, day=1)
            else:
                end_date = self.start_date.replace(month=self.start_date.month + 1, day=1)
        elif self.period == 'yearly':
            start_date = self.start_date.replace(month=1, day=1)
            end_date = self.start_date.replace(year=self.start_date.year + 1, month=1, day=1)
        else:  # quarterly
            quarter = (self.start_date.month - 1) // 3
            start_month = quarter * 3 + 1
            start_date = self.start_date.replace(month=start_month, day=1)
            if start_month == 10:  # Q4
                end_date = self.start_date.replace(year=self.start_date.year + 1, month=1, day=1)
            else:
                end_date = self.start_date.replace(month=start_month + 3, day=1)
        
        spent = Transaction.objects.filter(
            user=self.user,
            category=self.category,
            transaction_type='expense',
            date__gte=start_date,
            date__lt=end_date
        ).aggregate(total=Sum('amount'))['total']
        
        return spent or 0

    def get_remaining_amount(self):
        """Calculate remaining budget amount"""
        return self.amount - self.get_spent_amount()

    def get_usage_percentage(self):
        """Calculate budget usage percentage"""
        if self.amount == 0:
            return 0
        return (self.get_spent_amount() / self.amount) * 100