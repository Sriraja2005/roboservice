from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from services.models import Customer, ServiceItem, ServiceInward, ServiceLedger
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Set up local environment with sample data and admin user'

    def handle(self, *args, **options):
        self.stdout.write('Setting up local environment...')
        
        # Create admin user if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@robodigital.com',
                password='admin123'
            )
            self.stdout.write(
                self.style.SUCCESS('Admin user created!')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Admin user already exists!')
            )
        
        # Create sample customer if not exists
        customer, created = Customer.objects.get_or_create(
            phone='+1-555-0101',
            defaults={
                'name': 'John Smith',
                'email': 'john.smith@email.com',
                'address': '123 Main Street, City, State 12345'
            }
        )
        
        if created:
            self.stdout.write('Sample customer created!')
        
        # Create sample service if not exists
        service, created = ServiceItem.objects.get_or_create(
            customer=customer,
            device_type='laptop',
            brand='Dell',
            model='Latitude 5520',
            defaults={
                'serial_number': 'DL123456789',
                'problem_description': 'Laptop not turning on, suspected power supply issue',
                'accessories_received': 'Laptop, Charger, Mouse',
                'estimated_cost': 150.00,
                'actual_cost': 120.00,
                'status': 'completed',
                'payment_status': 'received',
                'received_date': timezone.now() - timedelta(days=5),
                'completed_date': timezone.now() - timedelta(days=2),
                'technician_notes': 'Replaced power supply unit. System working properly now.',
                'problem_resolved': 'Replaced faulty power supply unit with new one. System now boots normally.'
            }
        )
        
        if created:
            # Create inward entry
            inward = ServiceInward.objects.create(
                service_item=service,
                inward_number='RDC0001',
                received_by='Admin',
                condition_on_receipt='Device received in good condition',
                estimated_delivery_date=timezone.now().date() + timedelta(days=7)
            )
            
            # Create ledger entries
            ServiceLedger.objects.create(
                service_item=service,
                transaction_type='inward',
                description='Service inward created - laptop',
                amount=service.estimated_cost,
                notes=f'Inward number: {inward.inward_number}'
            )
            
            ServiceLedger.objects.create(
                service_item=service,
                transaction_type='completion',
                description='Service completed successfully',
                amount=service.actual_cost,
                notes='Device repaired and tested'
            )
            
            ServiceLedger.objects.create(
                service_item=service,
                transaction_type='payment',
                description='Payment received',
                amount=service.actual_cost,
                notes='Full payment received'
            )
            
            self.stdout.write('Sample service created!')
        
        self.stdout.write(
            self.style.SUCCESS('Local environment setup complete!')
        )
        self.stdout.write('Login credentials:')
        self.stdout.write('Username: admin')
        self.stdout.write('Password: admin123')
        self.stdout.write('URL: http://127.0.0.1:8000/') 