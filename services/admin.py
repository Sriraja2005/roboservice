from django.contrib import admin
from django.utils.html import format_html
from .models import Customer, ServiceItem, ServiceInward, ServiceLedger, ServiceExpense

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'created_at']
    search_fields = ['name', 'phone', 'email']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(ServiceItem)
class ServiceItemAdmin(admin.ModelAdmin):
    list_display = ['customer', 'device_type', 'brand', 'model', 'status', 'received_date', 'estimated_cost', 'actual_cost']
    list_filter = ['device_type', 'status', 'received_date', 'brand']
    search_fields = ['customer__name', 'brand', 'model', 'serial_number']
    readonly_fields = ['received_date', 'created_at', 'updated_at']
    date_hierarchy = 'received_date'
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer',)
        }),
        ('Device Information', {
            'fields': ('device_type', 'brand', 'model', 'serial_number')
        }),
        ('Service Details', {
            'fields': ('problem_description', 'accessories_received', 'technician_notes')
        }),
        ('Cost Information', {
            'fields': ('estimated_cost', 'actual_cost')
        }),
        ('Status Information', {
            'fields': ('status', 'received_date', 'completed_date', 'delivered_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ServiceInward)
class ServiceInwardAdmin(admin.ModelAdmin):
    list_display = ['inward_number', 'service_item', 'received_by', 'estimated_delivery_date', 'created_at']
    list_filter = ['created_at', 'estimated_delivery_date']
    search_fields = ['inward_number', 'service_item__customer__name', 'received_by']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'

@admin.register(ServiceLedger)
class ServiceLedgerAdmin(admin.ModelAdmin):
    list_display = ['service_item', 'transaction_type', 'amount', 'date', 'created_by']
    list_filter = ['transaction_type', 'date', 'created_by']
    search_fields = ['service_item__customer__name', 'description', 'notes']
    readonly_fields = ['date']
    date_hierarchy = 'date'

@admin.register(ServiceExpense)
class ServiceExpenseAdmin(admin.ModelAdmin):
    list_display = ['service_item', 'expense_type', 'amount', 'date']
    list_filter = ['expense_type', 'date']
    search_fields = ['service_item__customer__name', 'expense_type', 'description']
    readonly_fields = ['created_at']
    date_hierarchy = 'date'
