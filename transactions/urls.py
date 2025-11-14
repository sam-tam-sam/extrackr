from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    # Transaction CRUD
    path('', views.transaction_list, name='list'),
    path('add/', views.add_transaction, name='add'),
    path('edit/<int:pk>/', views.edit_transaction, name='edit'),
    path('delete/<int:pk>/', views.delete_transaction, name='delete'),
    
    # Budget management
    path('budgets/', views.budget_list, name='budgets'),
    path('budgets/add/', views.add_budget, name='add_budget'),
    path('budgets/edit/<int:pk>/', views.edit_budget, name='edit_budget'),
    path('budgets/delete/<int:pk>/', views.delete_budget, name='delete_budget'),
    
    # Recurring transactions
    path('recurring/', views.recurring_list, name='recurring'),
    path('recurring/add/', views.add_recurring, name='add_recurring'),
    path('recurring/edit/<int:pk>/', views.edit_recurring, name='edit_recurring'),
    path('recurring/delete/<int:pk>/', views.delete_recurring, name='delete_recurring'),
    
    # API endpoints
    path('api/stats/', views.get_transaction_stats, name='api_stats'),
    path('api/monthly-trend/', views.get_monthly_trend, name='api_monthly_trend'),
    path('api/category-breakdown/', views.get_category_breakdown, name='api_category_breakdown'),
]