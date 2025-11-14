#!/usr/bin/env python3
"""
Demo script to showcase extrackr functionality
Run this script to see the key features in action
"""

import os
import sys
import django

# Add the project to the Python path
project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_path)

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'extrackr_project.settings')
django.setup()

from django.contrib.auth.models import User
from transactions.models import Transaction, Category, Budget
from django.db.models import Sum


def main():
    print("🚀 extrackr - Personal Finance Tracker Demo")
    print("=" * 50)
    
    # Check if users exist
    users = User.objects.all()
    if not users.exists():
        print("❌ No users found. Please run 'python manage.py create_sample_data' first.")
        return
    
    print(f"✅ Found {users.count()} users")
    
    # Get demo user
    try:
        demo_user = User.objects.get(username='demo')
        print(f"👤 Using demo user: {demo_user.get_full_name() or demo_user.username}")
    except User.DoesNotExist:
        demo_user = users.first()
        print(f"👤 Using first available user: {demo_user.get_full_name() or demo_user.username}")
    
    print("\n" + "=" * 50)
    print("📊 FINANCIAL OVERVIEW")
    print("=" * 50)
    
    # Calculate financial summary
    income = Transaction.objects.filter(
        user=demo_user,
        transaction_type='income'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    expenses = Transaction.objects.filter(
        user=demo_user,
        transaction_type='expense'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    balance = income - expenses
    
    print(f"💰 Total Income:    ${income:,.2f}")
    print(f"💸 Total Expenses:  ${expenses:,.2f}")
    print(f"💳 Net Balance:     ${balance:,.2f}")
    
    print("\n" + "=" * 50)
    print("🏷️ CATEGORY BREAKDOWN")
    print("=" * 50)
    
    # Category breakdown
    categories = Category.objects.filter(
        transactions__user=demo_user,
        transactions__transaction_type='expense'
    ).distinct()
    
    for category in categories:
        cat_total = Transaction.objects.filter(
            user=demo_user,
            category=category,
            transaction_type='expense'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        if cat_total > 0:
            percentage = (cat_total / expenses) * 100 if expenses > 0 else 0
            print(f"{category.icon or '📊'} {category.name:<20}: ${cat_total:>8.2f} ({percentage:>5.1f}%)")
    
    print("\n" + "=" * 50)
    print("📈 RECENT TRANSACTIONS")
    print("=" * 50)
    
    # Recent transactions
    recent_transactions = Transaction.objects.filter(
        user=demo_user
    ).order_by('-date', '-created_at')[:10]
    
    for transaction in recent_transactions:
        amount_str = f"${transaction.amount:,.2f}"
        if transaction.transaction_type == 'income':
            amount_str = f"+{amount_str}"
        else:
            amount_str = f"-{amount_str}"
        
        print(f"📅 {transaction.date} | {transaction.category.name:<15} | {amount_str:>12}")
        if transaction.description:
            print(f"   {transaction.description}")
    
    print("\n" + "=" * 50)
    print("🎯 BUDGET STATUS")
    print("=" * 50)
    
    # Budget overview
    budgets = Budget.objects.filter(user=demo_user, is_active=True)
    
    for budget in budgets:
        spent = budget.get_spent_amount()
        remaining = budget.get_remaining_amount()
        usage_percent = budget.get_usage_percentage()
        
        status_icon = "✅" if usage_percent < 75 else "⚠️" if usage_percent < 90 else "🚨"
        
        print(f"{status_icon} {budget.category.name}")
        print(f"   Budget: ${budget.amount:,.2f} | Spent: ${spent:,.2f} | Remaining: ${remaining:,.2f}")
        print(f"   Usage: {usage_percent:.1f}%")
        print()
    
    print("=" * 50)
    print("✨ FEATURE HIGHLIGHTS")
    print("=" * 50)
    
    features = [
        "🔐 User Authentication & Profile Management",
        "💳 Income & Expense Tracking",
        "🏷️ Category Management with Icons & Colors",
        "🎯 Budget Setting & Monitoring",
        "🔄 Recurring Transactions",
        "📊 Interactive Charts & Analytics",
        "📄 PDF & Excel Report Generation",
        "📱 Responsive Design (Mobile + Desktop)",
        "🐳 Docker Support",
        "🔧 Django Admin Interface",
        "📈 Real-time Financial Analytics",
        "🔍 Advanced Filtering & Search"
    ]
    
    for feature in features:
        print(f"✅ {feature}")
    
    print("\n" + "=" * 50)
    print("🚀 READY TO USE!")
    print("=" * 50)
    print("To start the development server:")
    print("  python manage.py runserver")
    print("\nThen visit: http://localhost:8000")
    print("\nAdmin panel: http://localhost:8000/admin")
    print("Demo login: username='demo', password='demo123'")
    print("Admin login: username='admin', password='admin123'")


if __name__ == "__main__":
    main()