from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from django.http import JsonResponse
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from django import forms
from .models import Customer, ServiceItem, ServiceInward, ServiceLedger, ServiceExpense
from .forms import CustomerForm, ServiceItemForm, ServiceInwardForm, ServiceLedgerForm, ServiceExpenseForm

def dashboard(request):
    """Main dashboard view"""
    # Get statistics
    total_customers = Customer.objects.count()
    total_services = ServiceItem.objects.count()
    pending_services = ServiceItem.objects.filter(status='pending').count()
    in_progress_services = ServiceItem.objects.filter(status='in_progress').count()
    completed_services = ServiceItem.objects.filter(status='completed').count()
    delivered_services = ServiceItem.objects.filter(status='delivered').count()
    
    # Revenue statistics
    total_revenue = ServiceItem.objects.aggregate(total=Sum('actual_cost'))['total'] or 0
    this_month_revenue = ServiceItem.objects.filter(
        completed_date__month=timezone.now().month,
        completed_date__year=timezone.now().year
    ).aggregate(total=Sum('actual_cost'))['total'] or 0
    
    # Device type statistics
    device_stats = ServiceItem.objects.values('device_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Recent services
    recent_services = ServiceItem.objects.select_related('customer').order_by('-received_date')[:10]
    
    # Services due for delivery
    overdue_services = ServiceItem.objects.filter(
        status__in=['pending', 'in_progress'],
        received_date__lt=timezone.now() - timedelta(days=7)
    ).select_related('customer')[:5]
    
    context = {
        'total_customers': total_customers,
        'total_services': total_services,
        'pending_services': pending_services,
        'in_progress_services': in_progress_services,
        'completed_services': completed_services,
        'delivered_services': delivered_services,
        'total_revenue': total_revenue,
        'this_month_revenue': this_month_revenue,
        'device_stats': device_stats,
        'recent_services': recent_services,
        'overdue_services': overdue_services,
    }
    
    return render(request, 'services/dashboard.html', context)

def service_inward_list(request):
    """Service inward list view"""
    search_query = request.GET.get('search', '')
    device_type = request.GET.get('device_type', '')
    status = request.GET.get('status', '')
    
    services = ServiceItem.objects.select_related('customer').all()
    
    if search_query:
        services = services.filter(
            Q(customer__name__icontains=search_query) |
            Q(brand__icontains=search_query) |
            Q(model__icontains=search_query) |
            Q(serial_number__icontains=search_query)
        )
    
    if device_type:
        services = services.filter(device_type=device_type)
    
    if status:
        services = services.filter(status=status)
    
    # Pagination
    paginator = Paginator(services, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'device_type': device_type,
        'status': status,
        'device_types': ServiceItem.DEVICE_TYPES,
        'status_choices': ServiceItem.STATUS_CHOICES,
    }
    
    return render(request, 'services/service_inward_list.html', context)

def service_ledger(request, service_id=None):
    """Service ledger view"""
    if service_id:
        service_item = get_object_or_404(ServiceItem, id=service_id)
        ledger_entries = ServiceLedger.objects.filter(service_item=service_item).order_by('-date')
        expenses = ServiceExpense.objects.filter(service_item=service_item).order_by('-date')
        
        # Calculate totals
        total_ledger_amount = ledger_entries.aggregate(total=Sum('amount'))['total'] or 0
        total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
        
        context = {
            'service_item': service_item,
            'ledger_entries': ledger_entries,
            'expenses': expenses,
            'total_ledger_amount': total_ledger_amount,
            'total_expenses': total_expenses,
        }
        return render(request, 'services/service_ledger_detail.html', context)
    else:
        # Show all ledger entries
        ledger_entries = ServiceLedger.objects.select_related('service_item__customer').order_by('-date')
        
        # Pagination
        paginator = Paginator(ledger_entries, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'page_obj': page_obj,
        }
        return render(request, 'services/service_ledger.html', context)

def add_service_inward(request):
    """Add new service inward"""
    if request.method == 'POST':
        customer_form = CustomerForm(request.POST, prefix='customer')
        service_form = ServiceItemForm(request.POST, prefix='service')
        inward_form = ServiceInwardForm(request.POST, prefix='inward')
        
        # Check form validity and show errors
        customer_valid = customer_form.is_valid()
        service_valid = service_form.is_valid()
        inward_valid = inward_form.is_valid()
        
        if customer_valid and service_valid and inward_valid:
            customer = customer_form.save()
            service_item = service_form.save(commit=False)
            service_item.customer = customer
            service_item.actual_cost = 0.00  # Set default actual cost to 0
            service_item.save()
            
            inward = inward_form.save(commit=False)
            inward.service_item = service_item
            inward.save()
            
            # Create initial ledger entry
            ServiceLedger.objects.create(
                service_item=service_item,
                transaction_type='inward',
                description=f'Service inward created - {service_item.device_type}',
                amount=service_item.estimated_cost,
                notes=f'Inward number: {inward.inward_number}'
            )
            
            messages.success(request, 'Service inward created successfully!')
            return redirect('services:service_inward_list')
        else:
            # Show form errors
            if not customer_valid:
                messages.error(request, 'Please correct the customer information errors.')
            if not service_valid:
                messages.error(request, 'Please correct the service information errors.')
            if not inward_valid:
                messages.error(request, 'Please correct the inward information errors.')
    else:
        customer_form = CustomerForm(prefix='customer')
        service_form = ServiceItemForm(prefix='service')
        inward_form = ServiceInwardForm(prefix='inward')
    
    context = {
        'customer_form': customer_form,
        'service_form': service_form,
        'inward_form': inward_form,
    }
    
    return render(request, 'services/add_service_inward.html', context)

def edit_service(request, service_id):
    """Edit service item"""
    service_item = get_object_or_404(ServiceItem, id=service_id)
    
    if request.method == 'POST':
        form = ServiceItemForm(request.POST, instance=service_item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service updated successfully!')
            return redirect('services:service_inward_list')
    else:
        # Create form with all fields including actual_cost for editing
        form = ServiceItemForm(instance=service_item)
        # Add actual_cost field to the form
        form.fields['actual_cost'] = forms.DecimalField(
            max_digits=10, 
            decimal_places=2, 
            required=False,
            widget=forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '₹0.00'
            })
        )
    
    context = {
        'form': form,
        'service_item': service_item,
    }
    
    return render(request, 'services/edit_service.html', context)

def add_ledger_entry(request, service_id):
    """Add ledger entry for a service"""
    service_item = get_object_or_404(ServiceItem, id=service_id)
    
    if request.method == 'POST':
        form = ServiceLedgerForm(request.POST)
        if form.is_valid():
            ledger_entry = form.save(commit=False)
            ledger_entry.service_item = service_item
            ledger_entry.save()
            messages.success(request, 'Ledger entry added successfully!')
            return redirect('services:service_ledger_detail', service_id=service_id)
    else:
        form = ServiceLedgerForm()
    
    context = {
        'form': form,
        'service_item': service_item,
    }
    
    return render(request, 'services/add_ledger_entry.html', context)

def add_expense(request, service_id):
    """Add expense for a service"""
    service_item = get_object_or_404(ServiceItem, id=service_id)
    
    if request.method == 'POST':
        form = ServiceExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.service_item = service_item
            expense.save()
            messages.success(request, 'Expense added successfully!')
            return redirect('services:service_ledger_detail', service_id=service_id)
    else:
        form = ServiceExpenseForm()
    
    context = {
        'form': form,
        'service_item': service_item,
    }
    
    return render(request, 'services/add_expense.html', context)

def update_service_status(request, service_id):
    """Update service status via AJAX"""
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        service_item = get_object_or_404(ServiceItem, id=service_id)
        new_status = request.POST.get('status')
        
        if new_status in dict(ServiceItem.STATUS_CHOICES):
            old_status = service_item.status
            service_item.status = new_status
            
            # Update completion/delivery dates
            if new_status == 'completed' and not service_item.completed_date:
                service_item.completed_date = timezone.now()
            elif new_status == 'delivered' and not service_item.delivered_date:
                service_item.delivered_date = timezone.now()
            
            service_item.save()
            
            # Create ledger entry for status change
            ServiceLedger.objects.create(
                service_item=service_item,
                transaction_type='progress',
                description=f'Status changed from {old_status} to {new_status}',
                amount=0.00,
                notes=f'Status update: {old_status} → {new_status}'
            )
            
            return JsonResponse({'success': True, 'new_status': new_status})
    
    return JsonResponse({'success': False})

def customer_list(request):
    """Customer list view"""
    search_query = request.GET.get('search', '')
    customers = Customer.objects.all()
    
    if search_query:
        customers = customers.filter(
            Q(name__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(customers, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Calculate statistics
    total_services = ServiceItem.objects.count()
    avg_services_per_customer = total_services / max(customers.count(), 1)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'total_services': total_services,
        'avg_services_per_customer': avg_services_per_customer,
    }
    
    return render(request, 'services/customer_list.html', context)

def customer_detail(request, customer_id):
    """Customer detail view"""
    customer = get_object_or_404(Customer, id=customer_id)
    services = ServiceItem.objects.filter(customer=customer).order_by('-received_date')
    
    # Calculate statistics
    total_spent = services.aggregate(total=Sum('actual_cost'))['total'] or 0
    pending_services = services.filter(status='pending').count()
    completed_services = services.filter(status__in=['completed', 'delivered']).count()
    
    # Device type counts
    laptop_count = services.filter(device_type='laptop').count()
    desktop_count = services.filter(device_type='desktop').count()
    printer_count = services.filter(device_type='printer').count()
    
    context = {
        'customer': customer,
        'services': services,
        'total_spent': total_spent,
        'pending_services': pending_services,
        'completed_services': completed_services,
        'laptop_count': laptop_count,
        'desktop_count': desktop_count,
        'printer_count': printer_count,
    }
    
    return render(request, 'services/customer_detail.html', context)

def print_service_report(request, service_id):
    """Print service report"""
    service_item = get_object_or_404(ServiceItem, id=service_id)
    ledger_entries = ServiceLedger.objects.filter(service_item=service_item).order_by('date')
    expenses = ServiceExpense.objects.filter(service_item=service_item).order_by('date')
    
    # Calculate totals
    total_amount = ledger_entries.aggregate(total=Sum('amount'))['total'] or 0
    total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
    
    context = {
        'service_item': service_item,
        'ledger_entries': ledger_entries,
        'expenses': expenses,
        'total_amount': total_amount,
        'total_expenses': total_expenses,
    }
    
    return render(request, 'services/print_service_report.html', context)
