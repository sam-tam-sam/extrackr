from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum
from .models import Category, Transaction, RecurringTransaction, Budget


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_type', 'color_preview', 'is_active', 'created_at')
    list_filter = ('category_type', 'is_active', 'created_at')
    search_fields = ('name',)
    list_editable = ('is_active',)
    
    def color_preview(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border-radius: 3px;"></div>',
            obj.color
        )
    color_preview.short_description = 'Color'


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_type', 'amount', 'category', 'date', 'created_at')
    list_filter = ('transaction_type', 'category', 'date', 'created_at')
    search_fields = ('user__username', 'user__email', 'description', 'category__name')
    date_hierarchy = 'date'
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('user', 'transaction_type', 'category', 'amount')
        }),
        ('Additional Information', {
            'fields': ('description', 'date'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(RecurringTransaction)
class RecurringTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_type', 'amount', 'category', 'frequency', 'next_occurrence', 'is_active')
    list_filter = ('transaction_type', 'category', 'frequency', 'is_active', 'created_at')
    search_fields = ('user__username', 'user__email', 'description', 'category__name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('user', 'transaction_type', 'category', 'amount', 'frequency')
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date', 'next_occurrence')
        }),
        ('Additional Information', {
            'fields': ('description', 'is_active'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'amount', 'period', 'start_date', 'usage_percentage', 'is_active')
    list_filter = ('period', 'is_active', 'created_at', 'category')
    search_fields = ('user__username', 'user__email', 'category__name')
    readonly_fields = ('created_at', 'updated_at', 'usage_percentage')
    
    fieldsets = (
        (None, {
            'fields': ('user', 'category', 'amount', 'period')
        }),
        ('Duration', {
            'fields': ('start_date', 'end_date', 'is_active')
        }),
        ('Statistics', {
            'fields': ('usage_percentage',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def usage_percentage(self, obj):
        percentage = obj.get_usage_percentage()
        color = 'green'
        if percentage > 90:
            color = 'red'
        elif percentage > 75:
            color = 'orange'
        return format_html(
            '<span style="color: {};">{:.1f}%</span>',
            color,
            percentage
        )
    usage_percentage.short_description = 'Usage %'