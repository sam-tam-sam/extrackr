from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
import json

from transactions.models import Transaction, Category, Budget
from .utils import generate_pdf_report, generate_excel_report


@login_required
def report_dashboard(request):
    """Main reports dashboard"""
    return render(request, 'reports/dashboard.html')


@login_required
def generate_report(request):
    """Generate custom reports"""
    if request.method == 'POST':
        report_type = request.POST.get('report_type')
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        format_type = request.POST.get('format', 'pdf')
        
        # Get transactions based on filters
        transactions = Transaction.objects.filter(user=request.user)
        
        if date_from:
            transactions = transactions.filter(date__gte=date_from)
        if date_to:
            transactions = transactions.filter(date__lte=date_to)
        
        if format_type == 'pdf':
            return generate_pdf_report(transactions, report_type, request.user)
        elif format_type == 'excel':
            return generate_excel_report(transactions, report_type, request.user)
    
    return render(request, 'reports/generate.html')


@login_required
def generate_pdf_report(request):
    """Generate PDF report"""
    # Get parameters
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    report_type = request.GET.get('type', 'summary')
    
    # Get transactions
    transactions = Transaction.objects.filter(user=request.user)
    
    if date_from:
        transactions = transactions.filter(date__gte=date_from)
    if date_to:
        transactions = transactions.filter(date__lte=date_to)
    
    # Generate PDF
    response = generate_pdf_report(transactions, report_type, request.user)
    return response


@login_required
def generate_excel_report(request):
    """Generate Excel report"""
    # Get parameters
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    report_type = request.GET.get('type', 'summary')
    
    # Get transactions
    transactions = Transaction.objects.filter(user=request.user)
    
    if date_from:
        transactions = transactions.filter(date__gte=date_from)
    if date_to:
        transactions = transactions.filter(date__lte=date_to)
    
    # Generate Excel
    response = generate_excel_report(transactions, report_type, request.user)
    return response


@login_required
def analytics_dashboard(request):
    """Analytics dashboard with charts and insights"""
    return render(request, 'reports/analytics.html')


@login_required
def income_expense_chart(request):
    """Get income vs expense data for charts"""
    period = request.GET.get('period', 'monthly')
    months = int(request.GET.get('months', 12))
    
    data = []
    
    for i in range(months):
        if period == 'monthly':
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
                'period': month_start.strftime('%b %Y'),
                'income': float(income),
                'expenses': float(expenses)
            })
    
    data.reverse()
    return JsonResponse({'data': data})


@login_required
def category_analysis(request):
    """Get category analysis data"""
    period = request.GET.get('period', 'current_month')
    
    # Determine date range
    if period == 'current_month':
        date_from = timezone.now().replace(day=1)
    elif period == 'last_month':
        date_from = (timezone.now() - timedelta(days=30)).replace(day=1)
        date_to = timezone.now().replace(day=1)
    elif period == 'last_3_months':
        date_from = timezone.now() - timedelta(days=90)
        date_to = timezone.now()
    else:
        date_from = timezone.now().replace(day=1)
    
    # Get category data
    category_data = Transaction.objects.filter(
        user=request.user,
        transaction_type='expense'
    )
    
    if period != 'all_time':
        category_data = category_data.filter(date__gte=date_from)
        if 'date_to' in locals():
            category_data = category_data.filter(date__lt=date_to)
    
    category_data = category_data.values('category__name').annotate(
        total=Sum('amount'),
        count=Sum(1)
    ).order_by('-total')
    
    data = []
    for item in category_data:
        data.append({
            'category': item['category__name'],
            'amount': float(item['total']),
            'count': item['count']
        })
    
    return JsonResponse({'data': data})


@login_required
def trends_analysis(request):
    """Get trends analysis data"""
    trend_type = request.GET.get('type', 'expenses')
    period = request.GET.get('period', '6months')
    
    # Determine date range
    if period == '1month':
        date_from = timezone.now() - timedelta(days=30)
    elif period == '3months':
        date_from = timezone.now() - timedelta(days=90)
    elif period == '6months':
        date_from = timezone.now() - timedelta(days=180)
    elif period == '1year':
        date_from = timezone.now() - timedelta(days=365)
    else:
        date_from = timezone.now() - timedelta(days=180)
    
    # Get trend data by week
    transactions = Transaction.objects.filter(
        user=request.user,
        transaction_type=trend_type,
        date__gte=date_from
    ).order_by('date')
    
    # Group by week
    weekly_data = {}
    for transaction in transactions:
        week_key = transaction.date.strftime('%Y-%W')
        if week_key not in weekly_data:
            weekly_data[week_key] = {
                'week': transaction.date.strftime('%b %d'),
                'amount': 0,
                'count': 0
            }
        weekly_data[week_key]['amount'] += float(transaction.amount)
        weekly_data[week_key]['count'] += 1
    
    data = list(weekly_data.values())
    
    return JsonResponse({
        'data': data,
        'trend_type': trend_type,
        'period': period
    })