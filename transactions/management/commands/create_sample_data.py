from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random

from transactions.models import Category, Transaction, Budget, RecurringTransaction


class Command(BaseCommand):
    help = 'Create sample data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create or get admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@extrackr.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Created admin user (username: admin, password: admin123)'))
        
        # Create sample user
        sample_user, created = User.objects.get_or_create(
            username='demo',
            defaults={
                'email': 'demo@extrackr.com',
                'first_name': 'Demo',
                'last_name': 'User'
            }
        )
        if created:
            sample_user.set_password('demo123')
            sample_user.save()
            self.stdout.write(self.style.SUCCESS('Created demo user (username: demo, password: demo123)'))
        
        # Create categories
        self.create_categories()
        
        # Create sample transactions
        self.create_sample_transactions(sample_user)
        
        # Create sample budgets
        self.create_sample_budgets(sample_user)
        
        # Create sample recurring transactions
        self.create_sample_recurring(sample_user)
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
    
    def create_categories(self):
        # Income categories
        income_categories = [
            {'name': 'Salary', 'category_type': 'income', 'icon': '💼', 'color': '#10B981'},
            {'name': 'Freelance', 'category_type': 'income', 'icon': '💻', 'color': '#3B82F6'},
            {'name': 'Investment', 'category_type': 'income', 'icon': '📈', 'color': '#8B5CF6'},
            {'name': 'Business', 'category_type': 'income', 'icon': '🏢', 'color': '#F59E0B'},
            {'name': 'Other Income', 'category_type': 'income', 'icon': '💰', 'color': '#6B7280'}
        ]
        
        # Expense categories
        expense_categories = [
            {'name': 'Food & Dining', 'category_type': 'expense', 'icon': '🍽️', 'color': '#EF4444'},
            {'name': 'Transportation', 'category_type': 'expense', 'icon': '🚗', 'color': '#EF4444'},
            {'name': 'Shopping', 'category_type': 'expense', 'icon': '🛍️', 'color': '#EF4444'},
            {'name': 'Bills & Utilities', 'category_type': 'expense', 'icon': '💡', 'color': '#EF4444'},
            {'name': 'Entertainment', 'category_type': 'expense', 'icon': '🎬', 'color': '#EF4444'},
            {'name': 'Healthcare', 'category_type': 'expense', 'icon': '🏥', 'color': '#EF4444'},
            {'name': 'Education', 'category_type': 'expense', 'icon': '📚', 'color': '#EF4444'},
            {'name': 'Travel', 'category_type': 'expense', 'icon': '✈️', 'color': '#EF4444'},
            {'name': 'Other Expenses', 'category_type': 'expense', 'icon': '💸', 'color': '#EF4444'}
        ]
        
        for cat_data in income_categories + expense_categories:
            Category.objects.get_or_create(
                name=cat_data['name'],
                category_type=cat_data['category_type'],
                defaults={
                    'icon': cat_data['icon'],
                    'color': cat_data['color']
                }
            )
        
        self.stdout.write(self.style.SUCCESS('Categories created'))
    
    def create_sample_transactions(self, user):
        # Get categories
        salary_cat = Category.objects.get(name='Salary', category_type='income')
        freelance_cat = Category.objects.get(name='Freelance', category_type='income')
        food_cat = Category.objects.get(name='Food & Dining', category_type='expense')
        transport_cat = Category.objects.get(name='Transportation', category_type='expense')
        shopping_cat = Category.objects.get(name='Shopping', category_type='expense')
        bills_cat = Category.objects.get(name='Bills & Utilities', category_type='expense')
        
        # Sample income transactions
        income_transactions = [
            {
                'user': user,
                'transaction_type': 'income',
                'category': salary_cat,
                'amount': 3500.00,
                'description': 'Monthly salary',
                'date': timezone.now().replace(day=1)
            },
            {
                'user': user,
                'transaction_type': 'income',
                'category': freelance_cat,
                'amount': 800.00,
                'description': 'Web development project',
                'date': timezone.now() - timedelta(days=5)
            },
            {
                'user': user,
                'transaction_type': 'income',
                'category': freelance_cat,
                'amount': 450.00,
                'description': 'Logo design project',
                'date': timezone.now() - timedelta(days=12)
            }
        ]
        
        # Sample expense transactions
        expense_transactions = [
            {
                'user': user,
                'transaction_type': 'expense',
                'category': food_cat,
                'amount': 85.50,
                'description': 'Grocery shopping',
                'date': timezone.now() - timedelta(days=2)
            },
            {
                'user': user,
                'transaction_type': 'expense',
                'category': transport_cat,
                'amount': 45.00,
                'description': 'Gas station',
                'date': timezone.now() - timedelta(days=3)
            },
            {
                'user': user,
                'transaction_type': 'expense',
                'category': shopping_cat,
                'amount': 120.00,
                'description': 'New shoes',
                'date': timezone.now() - timedelta(days=7)
            },
            {
                'user': user,
                'transaction_type': 'expense',
                'category': bills_cat,
                'amount': 150.00,
                'description': 'Electricity bill',
                'date': timezone.now() - timedelta(days=10)
            },
            {
                'user': user,
                'transaction_type': 'expense',
                'category': food_cat,
                'amount': 35.75,
                'description': 'Lunch at restaurant',
                'date': timezone.now() - timedelta(days=1)
            }
        ]
        
        # Create transactions
        for trans_data in income_transactions + expense_transactions:
            Transaction.objects.create(**trans_data)
        
        self.stdout.write(self.style.SUCCESS('Sample transactions created'))
    
    def create_sample_budgets(self, user):
        # Get expense categories
        food_cat = Category.objects.get(name='Food & Dining', category_type='expense')
        transport_cat = Category.objects.get(name='Transportation', category_type='expense')
        shopping_cat = Category.objects.get(name='Shopping', category_type='expense')
        
        # Sample budgets
        budgets = [
            {
                'user': user,
                'category': food_cat,
                'amount': 400.00,
                'period': 'monthly',
                'start_date': timezone.now().replace(day=1)
            },
            {
                'user': user,
                'category': transport_cat,
                'amount': 200.00,
                'period': 'monthly',
                'start_date': timezone.now().replace(day=1)
            },
            {
                'user': user,
                'category': shopping_cat,
                'amount': 300.00,
                'period': 'monthly',
                'start_date': timezone.now().replace(day=1)
            }
        ]
        
        for budget_data in budgets:
            Budget.objects.create(**budget_data)
        
        self.stdout.write(self.style.SUCCESS('Sample budgets created'))
    
    def create_sample_recurring(self, user):
        # Get categories
        salary_cat = Category.objects.get(name='Salary', category_type='income')
        bills_cat = Category.objects.get(name='Bills & Utilities', category_type='expense')
        
        # Sample recurring transactions
        recurring_transactions = [
            {
                'user': user,
                'transaction_type': 'income',
                'category': salary_cat,
                'amount': 3500.00,
                'description': 'Monthly salary',
                'frequency': 'monthly',
                'start_date': timezone.now().replace(day=1),
                'next_occurrence': timezone.now().replace(day=1) + timedelta(days=30)
            },
            {
                'user': user,
                'transaction_type': 'expense',
                'category': bills_cat,
                'amount': 150.00,
                'description': 'Monthly internet bill',
                'frequency': 'monthly',
                'start_date': timezone.now().replace(day=15),
                'next_occurrence': timezone.now().replace(day=15)
            }
        ]
        
        for recurring_data in recurring_transactions:
            RecurringTransaction.objects.create(**recurring_data)
        
        self.stdout.write(self.style.SUCCESS('Sample recurring transactions created'))