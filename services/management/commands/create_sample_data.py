from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from services.models import Customer, ServiceItem, ServiceInward, ServiceLedger, ServiceExpense

class Command(BaseCommand):
    help = 'Create sample data for testing the service management system'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create sample customers
        customers_data = [
            {
                'name': 'John Smith',
                'phone': '+1-555-0101',
                'email': 'john.smith@email.com',
                'address': '123 Main Street, City, State 12345'
            },
            {
                'name': 'Sarah Johnson',
                'phone': '+1-555-0102',
                'email': 'sarah.johnson@email.com',
                'address': '456 Oak Avenue, City, State 12345'
            },
            {
                'name': 'Mike Davis',
                'phone': '+1-555-0103',
                'email': 'mike.davis@email.com',
                'address': '789 Pine Road, City, State 12345'
            },
            {
                'name': 'Lisa Wilson',
                'phone': '+1-555-0104',
                'email': 'lisa.wilson@email.com',
                'address': '321 Elm Street, City, State 12345'
            },
            {
                'name': 'David Brown',
                'phone': '+1-555-0105',
                'email': 'david.brown@email.com',
                'address': '654 Maple Drive, City, State 12345'
            }
        ]
        
        customers = []
        for data in customers_data:
            customer, created = Customer.objects.get_or_create(
                phone=data['phone'],
                defaults=data
            )
            customers.append(customer)
            if created:
                self.stdout.write(f'Created customer: {customer.name}')
        
        # Create sample services
        services_data = [
            {
                'customer': customers[0],
                'device_type': 'laptop',
                'brand': 'Dell',
                'model': 'Latitude 5520',
                'serial_number': 'DL123456789',
                'problem_description': 'Laptop not turning on, suspected power supply issue',
                'accessories_received': 'Laptop, Charger, Mouse',
                'estimated_cost': 150.00,
                'actual_cost': 120.00,
                'status': 'completed',
                'received_date': timezone.now() - timedelta(days=5),
                'completed_date': timezone.now() - timedelta(days=2),
                'technician_notes': 'Replaced power supply unit. System working properly now.'
            },
            {
                'customer': customers[1],
                'device_type': 'desktop',
                'brand': 'HP',
                'model': 'Pavilion Desktop',
                'serial_number': 'HP987654321',
                'problem_description': 'Slow performance, needs RAM upgrade and virus removal',
                'accessories_received': 'Desktop tower, Monitor, Keyboard, Mouse',
                'estimated_cost': 200.00,
                'actual_cost': 180.00,
                'status': 'in_progress',
                'received_date': timezone.now() - timedelta(days=3),
                'technician_notes': 'Virus removed. RAM upgrade completed. Testing performance.'
            },
            {
                'customer': customers[2],
                'device_type': 'printer',
                'brand': 'Canon',
                'model': 'Pixma MG3620',
                'serial_number': 'CN456789123',
                'problem_description': 'Printer not printing, paper jam error',
                'accessories_received': 'Printer, Power cable, USB cable',
                'estimated_cost': 50.00,
                'actual_cost': 45.00,
                'status': 'delivered',
                'received_date': timezone.now() - timedelta(days=7),
                'completed_date': timezone.now() - timedelta(days=5),
                'delivered_date': timezone.now() - timedelta(days=4),
                'technician_notes': 'Cleared paper jam. Replaced worn rollers. Printer working fine.'
            },
            {
                'customer': customers[3],
                'device_type': 'laptop',
                'brand': 'Lenovo',
                'model': 'ThinkPad T14',
                'serial_number': 'LN789123456',
                'problem_description': 'Broken screen, needs replacement',
                'accessories_received': 'Laptop only',
                'estimated_cost': 300.00,
                'actual_cost': 0.00,
                'status': 'pending',
                'received_date': timezone.now() - timedelta(days=1),
                'technician_notes': 'Waiting for screen replacement part to arrive.'
            },
            {
                'customer': customers[4],
                'device_type': 'desktop',
                'brand': 'Apple',
                'model': 'iMac 27"',
                'serial_number': 'AP321654987',
                'problem_description': 'Software installation and system optimization',
                'accessories_received': 'iMac only',
                'estimated_cost': 100.00,
                'actual_cost': 100.00,
                'status': 'completed',
                'received_date': timezone.now() - timedelta(days=10),
                'completed_date': timezone.now() - timedelta(days=8),
                'technician_notes': 'Installed requested software. Optimized system performance.'
            }
        ]
        
        for data in services_data:
            service, created = ServiceItem.objects.get_or_create(
                customer=data['customer'],
                device_type=data['device_type'],
                brand=data['brand'],
                model=data['model'],
                serial_number=data['serial_number'],
                defaults=data
            )
            if created:
                self.stdout.write(f'Created service: {service.customer.name} - {service.device_type}')
                
                # Create inward entry
                inward_number = f"RDC{service.id:04d}"
                inward = ServiceInward.objects.create(
                    service_item=service,
                    inward_number=inward_number,
                    received_by='Admin',
                    condition_on_receipt='Device received in good condition',
                    estimated_delivery_date=timezone.now().date() + timedelta(days=7)
                )
                
                # Create initial ledger entry
                ServiceLedger.objects.create(
                    service_item=service,
                    transaction_type='inward',
                    description=f'Service inward created - {service.device_type}',
                    amount=service.estimated_cost,
                    notes=f'Inward number: {inward.inward_number}'
                )
                
                # Add some additional ledger entries for completed services
                if service.status in ['completed', 'delivered']:
                    ServiceLedger.objects.create(
                        service_item=service,
                        transaction_type='progress',
                        description='Work started on device',
                        amount=0.00,
                        notes='Initial diagnosis completed'
                    )
                    
                    ServiceLedger.objects.create(
                        service_item=service,
                        transaction_type='completion',
                        description='Service completed successfully',
                        amount=service.actual_cost,
                        notes='Device repaired and tested'
                    )
                    
                    if service.status == 'delivered':
                        ServiceLedger.objects.create(
                            service_item=service,
                            transaction_type='delivery',
                            description='Device delivered to customer',
                            amount=0.00,
                            notes='Customer satisfied with service'
                        )
                
                # Add some expenses for completed services
                if service.status in ['completed', 'delivered']:
                    ServiceExpense.objects.create(
                        service_item=service,
                        expense_type='Parts',
                        description='Replacement parts used',
                        amount=service.actual_cost * 0.6,
                        date=service.received_date.date()
                    )
                    
                    ServiceExpense.objects.create(
                        service_item=service,
                        expense_type='Labor',
                        description='Technician labor',
                        amount=service.actual_cost * 0.4,
                        date=service.received_date.date()
                    )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data!')
        )
        self.stdout.write(f'Created {len(customers)} customers and {len(services_data)} services') 