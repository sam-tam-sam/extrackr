from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    # Report dashboard
    path('', views.report_dashboard, name='dashboard'),
    
    # Report generation
    path('generate/', views.generate_report, name='generate'),
    path('pdf/', views.generate_pdf_report, name='pdf_report'),
    path('excel/', views.generate_excel_report, name='excel_report'),
    
    # Analytics
    path('analytics/', views.analytics_dashboard, name='analytics'),
    path('analytics/income-expense/', views.income_expense_chart, name='income_expense_chart'),
    path('analytics/category-analysis/', views.category_analysis, name='category_analysis'),
    path('analytics/trends/', views.trends_analysis, name='trends_analysis'),
]