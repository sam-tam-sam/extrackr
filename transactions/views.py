from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import timedelta
import json

from .models import Transaction, Category, Budget, RecurringTransaction
from .forms import TransactionForm, BudgetForm, RecurringTransactionForm


@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date', '-created_at')
    
    # Filter by type
    transaction_type = request.GET.get('type')
    if transaction_type:
        transactions = transactions.filter(transaction_type=transaction_type)
    
    # Filter by category
    category = request.GET.get('category')
    if category:
        transactions = transactions.filter(category_id=category)
    
    # Filter by date range
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        transactions = transactions.filter(date__gte=date_from)
    if date_to:
        transactions = transactions.filter(date__lte=date_to)
    
    # Search
    search = request.GET.get('search')
    if search:
        transactions = transactions.filter(
            Q(description__icontains=search) |
            Q(category__name__icontains=search)
        )
    
    categories = Category.objects.filter(is_active=True)
    
    return render(request, 'transactions/list.html', {
        'transactions': transactions,
        'categories': categories,
        'transaction_types': Transaction.TRANSACTION_TYPES
    })


@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Transaction added successfully!')
            return redirect('transactions:list')
    else:
        # Pre-set transaction type from URL parameter
        initial_type = request.GET.get('type', 'expense')
        form = TransactionForm(initial={'transaction_type': initial_type})
    
    return render(request, 'transactions/add.html', {
        'form': form,
        'categories': Category.objects.filter(is_active=True)
    })


@login_required
def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transaction updated successfully!')
            return redirect('transactions:list')
    else:
        form = TransactionForm(instance=transaction)
    
    return render(request, 'transactions/edit.html', {
        'form': form,
        'transaction': transaction,
        'categories': Category.objects.filter(is_active=True)
    })


@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transaction deleted successfully!')
        return redirect('transactions:list')
    
    return render(request, 'transactions/delete.html', {
        'transaction': transaction
    })


@login_required
def budget_list(request):
    budgets = Budget.objects.filter(user=request.user, is_active=True)
    
    # Calculate budget usage for each budget
    for budget in budgets:
        budget.spent_amount = budget.get_spent_amount()
        budget.remaining_amount = budget.get_remaining_amount()
        budget.usage_percentage = budget.get_usage_percentage()
    
    return render(request, 'transactions/budgets.html', {
        'budgets': budgets
    })


@login_required
def add_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            messages.success(request, 'Budget created successfully!')
            return redirect('transactions:budgets')
    else:
        form = BudgetForm()
    
    return render(request, 'transactions/add_budget.html', {
        'form': form,
        'expense_categories': Category.objects.filter(category_type='expense', is_active=True)
    })


@login_required
def edit_budget(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            messages.success(request, 'Budget updated successfully!')
            return redirect('transactions:budgets')
    else:
        form = BudgetForm(instance=budget)
    
    return render(request, 'transactions/edit_budget.html', {
        'form': form,
        'budget': budget,
        'expense_categories': Category.objects.filter(category_type='expense', is_active=True)
    })


@login_required
def delete_budget(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    
    if request.method == 'POST':
        budget.delete()
        messages.success(request, 'Budget deleted successfully!')
        return redirect('transactions:budgets')
    
    return render(request, 'transactions/delete_budget.html', {
        'budget': budget
    })


@login_required
def recurring_list(request):
    recurring_transactions = RecurringTransaction.objects.filter(user=request.user, is_active=True)
    
    return render(request, 'transactions/recurring.html', {
        'recurring_transactions': recurring_transactions
    })


@login_required
def add_recurring(request):
    if request.method == 'POST':
        form = RecurringTransactionForm(request.POST)
        if form.is_valid():
            recurring = form.save(commit=False)
            recurring.user = request.user
            recurring.save()
            messages.success(request, 'Recurring transaction created successfully!')
            return redirect('transactions:recurring')
    else:
        form = RecurringTransactionForm()
    
    return render(request, 'transactions/add_recurring.html', {
        'form': form,
        'categories': Category.objects.filter(is_active=True)
    })


@login_required
def edit_recurring(request, pk):
    recurring = get_object_or_404(RecurringTransaction, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = RecurringTransactionForm(request.POST, instance=recurring)
        if form.is_valid():
            form.save()
            messages.success(request, 'Recurring transaction updated successfully!')
            return redirect('transactions:recurring')
    else:
        form = RecurringTransactionForm(instance=recurring)
    
    return render(request, 'transactions/edit_recurring.html', {
        'form': form,
        'recurring': recurring,
        'categories': Category.objects.filter(is_active=True)
    })


@login_required
def delete_recurring(request, pk):
    recurring = get_object_or_404(RecurringTransaction, pk=pk, user=request.user)
    
    if request.method == 'POST':
        recurring.delete()
        messages.success(request, 'Recurring transaction deleted successfully!')
        return redirect('transactions:recurring')
    
    return render(request, 'transactions/delete_recurring.html', {
        'recurring': recurring
    })


# API Views
@login_required
def get_transaction_stats(request):
    """Get transaction statistics for dashboard"""
    user = request.user
    
    # Current month stats
    current_month = timezone.now().replace(day=1)
    
    income = Transaction.objects.filter(
        user=user,
        transaction_type='income',
        date__gte=current_month
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    expenses = Transaction.objects.filter(
        user=user,
        transaction_type='expense',
        date__gte=current_month
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Previous month for comparison
    prev_month = current_month - timedelta(days=1)
    prev_month = prev_month.replace(day=1)
    
    prev_income = Transaction.objects.filter(
        user=user,
        transaction_type='income',
        date__gte=prev_month,
        date__lt=current_month
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    prev_expenses = Transaction.objects.filter(
        user=user,
        transaction_type='expense',
        date__gte=prev_month,
        date__lt=current_month
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Calculate changes
    income_change = ((income - prev_income) / prev_income * 100) if prev_income > 0 else 0
    expense_change = ((expenses - prev_expenses) / prev_expenses * 100) if prev_expenses > 0 else 0
    
    return JsonResponse({
        'income': float(income),
        'expenses': float(expenses),
        'net_balance': float(income - expenses),
        'income_change': income_change,
        'expense_change': expense_change
    })


@login_required
def get_monthly_trend(request):
    """Get monthly trend data for charts"""
    months = int(request.GET.get('months', 6))
    
    # Generate monthly data
    data = []
    for i in range(months):
        date = timezone.now() - timedelta(days=30 * i)
        month_start = date.replace(day=1)
        
        income = Transaction.objects.filter(
            user=request.user,
            transaction_type='income',
            date__year=month_start.year,
            date__month=month_start.month
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        expenses = Transaction.objects.filter(
            user=request.user,
            transaction_type='expense',
            date__year=month_start.year,
            date__month=month_start.month
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        data.append({
            'month': month_start.strftime('%b %Y'),
            'income': float(income),
            'expenses': float(expenses)
        })
    
    data.reverse()
    return JsonResponse({'data': data})


@login_required
def get_category_breakdown(request):
    """Get category breakdown data for charts"""
    # Get current month expenses by category
    current_month = timezone.now().replace(day=1)
    
    category_data = Transaction.objects.filter(
        user=request.user,
        transaction_type='expense',
        date__gte=current_month
    ).values('category__name').annotate(
        total=Sum('amount')
    ).order_by('-total')
    
    data = []
    for item in category_data:
        data.append({
            'category': item['category__name'],
            'amount': float(item['total'])
        })
    
    return JsonResponse({'data': data})