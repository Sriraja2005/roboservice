from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Customer(models.Model):
    """Customer information model"""
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

class ServiceItem(models.Model):
    """Service item model for laptops, desktops, and printers"""
    DEVICE_TYPES = [
        ('laptop', 'Laptop'),
        ('desktop', 'Desktop'),
        ('printer', 'Printer'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Payment Pending'),
        ('received', 'Payment Received'),
        ('partial', 'Partial Payment'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='service_items')
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPES)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    problem_description = models.TextField()
    accessories_received = models.TextField(blank=True, null=True)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    received_date = models.DateTimeField(auto_now_add=True)
    completed_date = models.DateTimeField(blank=True, null=True)
    delivered_date = models.DateTimeField(blank=True, null=True)
    technician_notes = models.TextField(blank=True, null=True)
    problem_resolved = models.TextField(blank=True, null=True, help_text="Description of how the problem was resolved")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.name} - {self.device_type} ({self.brand} {self.model})"

    class Meta:
        ordering = ['-received_date']

class ServiceInward(models.Model):
    """Service inward entry model"""
    service_item = models.OneToOneField(ServiceItem, on_delete=models.CASCADE, related_name='inward_entry')
    inward_number = models.CharField(max_length=20, unique=True)
    received_by = models.CharField(max_length=100)
    condition_on_receipt = models.TextField()
    estimated_delivery_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inward #{self.inward_number} - {self.service_item}"

    class Meta:
        ordering = ['-created_at']

class ServiceLedger(models.Model):
    """Service ledger for tracking all service transactions"""
    TRANSACTION_TYPES = [
        ('inward', 'Service Inward'),
        ('progress', 'Work Progress'),
        ('completion', 'Service Completion'),
        ('delivery', 'Service Delivery'),
        ('payment', 'Payment'),
    ]

    service_item = models.ForeignKey(ServiceItem, on_delete=models.CASCADE, related_name='ledger_entries')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    created_by = models.CharField(max_length=100, default='System')

    def __str__(self):
        return f"{self.service_item} - {self.transaction_type} - {self.date.strftime('%Y-%m-%d')}"

    class Meta:
        ordering = ['-date']

class ServiceExpense(models.Model):
    """Model to track expenses for each service"""
    service_item = models.ForeignKey(ServiceItem, on_delete=models.CASCADE, related_name='expenses')
    expense_type = models.CharField(max_length=100)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service_item} - {self.expense_type} - ${self.amount}"

    class Meta:
        ordering = ['-date']
