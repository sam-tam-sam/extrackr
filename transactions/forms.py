from django import forms
from django.core.validators import MinValueValidator
from .models import Transaction, Budget, RecurringTransaction, Category


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['transaction_type', 'category', 'amount', 'description', 'date']
        widgets = {
            'transaction_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter transaction description (optional)'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            })
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filter categories based on transaction type
        if 'transaction_type' in self.data:
            try:
                transaction_type = self.data.get('transaction_type')
                self.fields['category'].queryset = Category.objects.filter(
                    category_type=transaction_type,
                    is_active=True
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['category'].queryset = Category.objects.filter(
                category_type=self.instance.transaction_type,
                is_active=True
            )
        else:
            # Default to expense categories
            self.fields['category'].queryset = Category.objects.filter(
                category_type='expense',
                is_active=True
            )


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount', 'period', 'start_date', 'end_date']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01'
            }),
            'period': forms.Select(attrs={
                'class': 'form-control'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            })
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Only show expense categories for budgets
        self.fields['category'].queryset = Category.objects.filter(
            category_type='expense',
            is_active=True
        )
        
        self.fields['end_date'].required = False


class RecurringTransactionForm(forms.ModelForm):
    class Meta:
        model = RecurringTransaction
        fields = ['transaction_type', 'category', 'amount', 'description', 'frequency', 'start_date', 'end_date']
        widgets = {
            'transaction_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter description (optional)'
            }),
            'frequency': forms.Select(attrs={
                'class': 'form-control'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            })
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filter categories based on transaction type
        if 'transaction_type' in self.data:
            try:
                transaction_type = self.data.get('transaction_type')
                self.fields['category'].queryset = Category.objects.filter(
                    category_type=transaction_type,
                    is_active=True
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['category'].queryset = Category.objects.filter(
                category_type=self.instance.transaction_type,
                is_active=True
            )
        else:
            # Default to expense categories
            self.fields['category'].queryset = Category.objects.filter(
                category_type='expense',
                is_active=True
            )
        
        self.fields['end_date'].required = False