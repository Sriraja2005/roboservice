from django import forms
from django.core.validators import MinValueValidator
from decimal import Decimal
from .models import Customer, ServiceItem, ServiceInward, ServiceLedger, ServiceExpense

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email', 'address']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter customer name'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter customer address'
            }),
        }

class ServiceItemForm(forms.ModelForm):
    class Meta:
        model = ServiceItem
        fields = [
            'device_type', 'brand', 'model', 'serial_number',
            'problem_description', 'accessories_received',
            'estimated_cost', 'technician_notes', 'problem_resolved', 'payment_status'
        ]
        widgets = {
            'device_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'brand': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter device brand'
            }),
            'model': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter device model'
            }),
            'serial_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter serial number (optional)'
            }),
            'problem_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe the problem in detail'
            }),
            'accessories_received': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'List accessories received (optional)'
            }),
            'estimated_cost': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '₹0.00'
            }),
            'technician_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add technician notes (optional)'
            }),
            'problem_resolved': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe how the problem was resolved (optional)'
            }),
            'payment_status': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

class ServiceInwardForm(forms.ModelForm):
    class Meta:
        model = ServiceInward
        fields = ['inward_number', 'received_by', 'condition_on_receipt', 'estimated_delivery_date']
        widgets = {
            'inward_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Auto-generated (RDC format)',
                'readonly': 'readonly'
            }),
            'received_by': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter name of person who received'
            }),
            'condition_on_receipt': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe the condition of the device when received'
            }),
            'estimated_delivery_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

class ServiceLedgerForm(forms.ModelForm):
    class Meta:
        model = ServiceLedger
        fields = ['transaction_type', 'description', 'amount', 'notes']
        widgets = {
            'transaction_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter transaction description'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '₹0.00'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Additional notes (optional)'
            }),
        }

class ServiceExpenseForm(forms.ModelForm):
    class Meta:
        model = ServiceExpense
        fields = ['expense_type', 'description', 'amount', 'date']
        widgets = {
            'expense_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Parts, Labor, Shipping'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe the expense'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': '₹0.00'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

class ServiceStatusUpdateForm(forms.Form):
    status = forms.ChoiceField(
        choices=ServiceItem.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    notes = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Add notes about the status change (optional)'
        }),
        required=False
    )

class ServiceSearchForm(forms.Form):
    search = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by customer, brand, model, or serial number'
        }),
        required=False
    )
    device_type = forms.ChoiceField(
        choices=[('', 'All Devices')] + ServiceItem.DEVICE_TYPES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    status = forms.ChoiceField(
        choices=[('', 'All Status')] + ServiceItem.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    date_from = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        required=False
    )
    date_to = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        required=False
    ) 