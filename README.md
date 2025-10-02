# Service Management System

A comprehensive Django web application for managing service inward lists and creating service ledgers for laptops, desktops, and printers.

## Features

### 🏠 Dashboard
- Overview statistics (total customers, services, revenue)
- Service status distribution
- Recent services list
- Overdue services alerts
- Device type statistics

### 📋 Service Inward Management
- Add new service inward entries
- Customer information management
- Device details (laptop, desktop, printer)
- Problem description and accessories tracking
- Status tracking (pending, in progress, completed, delivered)
- Search and filter functionality

### 📊 Service Ledger
- Complete transaction history for each service
- Expense tracking
- Payment records
- Work progress updates
- Service completion and delivery tracking

### 👥 Customer Management
- Customer database with contact information
- Service history per customer
- Customer search and filtering

### 🔧 Admin Panel
- Full Django admin interface
- Data management and export
- User management

## Technology Stack

- **Backend**: Django 5.2.5
- **Database**: SQLite (can be changed to PostgreSQL/MySQL)
- **Frontend**: Bootstrap 5, jQuery
- **Icons**: Bootstrap Icons

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or download the project**
   ```bash
   # If you have the project files, navigate to the project directory
   cd service
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   ```bash
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser (admin account)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main application: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Usage

### Getting Started

1. **Login to Admin Panel**
   - Go to http://127.0.0.1:8000/admin/
   - Use your superuser credentials

2. **Add Your First Service Inward**
   - Click "New Service Inward" from the dashboard
   - Fill in customer information
   - Add device details (laptop, desktop, or printer)
   - Describe the problem
   - Set estimated cost and delivery date

3. **Track Service Progress**
   - Update service status as work progresses
   - Add ledger entries for work updates
   - Record expenses and payments

4. **View Service Ledger**
   - Access complete transaction history
   - Track all expenses and payments
   - Monitor service progress

### Key Features

#### Service Inward Process
1. **Customer Registration**: Add new customer or select existing
2. **Device Information**: Specify device type, brand, model, serial number
3. **Problem Description**: Detailed description of the issue
4. **Accessories**: List any accessories received with the device
5. **Cost Estimation**: Set estimated and actual costs
6. **Status Tracking**: Monitor progress through different stages

#### Service Ledger Management
- **Inward Entry**: Automatic creation when service is added
- **Progress Updates**: Track work progress and status changes
- **Expense Recording**: Add parts, labor, and other expenses
- **Payment Tracking**: Record customer payments
- **Completion Notes**: Add final notes and delivery information

## Database Models

### Customer
- Name, phone, email, address
- Creation and update timestamps

### ServiceItem
- Device type (laptop, desktop, printer)
- Brand, model, serial number
- Problem description and accessories
- Estimated and actual costs
- Status tracking with timestamps

### ServiceInward
- Inward number and received by information
- Condition on receipt
- Estimated delivery date

### ServiceLedger
- Transaction types (inward, progress, completion, delivery, payment)
- Amount tracking
- Notes and descriptions

### ServiceExpense
- Expense type and description
- Amount and date
- Linked to specific service

## Customization

### Adding New Device Types
1. Edit `services/models.py`
2. Add new choices to `DEVICE_TYPES` in `ServiceItem` model
3. Run migrations

### Modifying Status Workflow
1. Edit `STATUS_CHOICES` in `ServiceItem` model
2. Update templates to reflect new statuses
3. Run migrations

### Styling Changes
- Modify CSS in `templates/base.html`
- Update Bootstrap classes in templates
- Add custom CSS files to `static/` directory

## Deployment

### Production Setup
1. **Change DEBUG setting**
   ```python
   # settings.py
   DEBUG = False
   ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
   ```

2. **Use a production database**
   ```python
   # settings.py
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_db_name',
           'USER': 'your_db_user',
           'PASSWORD': 'your_db_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

3. **Configure static files**
   ```bash
   python manage.py collectstatic
   ```

4. **Use a production server**
   - Gunicorn with Nginx
   - Apache with mod_wsgi
   - Heroku, DigitalOcean, AWS, etc.

## Support

For issues and questions:
1. Check the Django documentation
2. Review the code comments
3. Check the admin panel for data management

## License

This project is open source and available under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Note**: This is a development version. For production use, ensure proper security measures, backup strategies, and performance optimization. 