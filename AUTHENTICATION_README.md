# Service Management System - Authentication

## 🔐 User Authentication System

This service management system now requires user authentication. Only logged-in users can access the system, and only administrators can create new users.

## 👤 Default Admin User

**Username:** `admin`  
**Password:** `admin123`  
**Email:** `admin@robodigital.com`

## 🚀 Quick Start

### 1. Start the Server
```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run the server
py manage.py runserver
```

### 2. Access the System
- Open your browser and go to: `http://127.0.0.1:8000/`
- You will be redirected to the login page
- Use the default admin credentials to log in

### 3. Create New Users (Admin Only)
- Log in as admin
- Go to Admin Panel: `http://127.0.0.1:8000/admin/`
- Navigate to "Users" section
- Click "Add User" to create new users

## 🔧 Management Commands

### Create Admin User
```bash
py manage.py create_admin_user
```

### Reset Admin Password
```bash
py manage.py reset_admin_password
```

### Create Sample Data
```bash
py manage.py create_sample_data
```

## 🛡️ Security Features

- **Login Required:** All pages require authentication
- **Admin-Only User Creation:** Only admins can create new users
- **CSRF Protection:** All forms are protected against CSRF attacks
- **Session Management:** Secure session handling
- **Password Validation:** Strong password requirements

## 📱 User Interface

### Login Page
- Modern, responsive design
- Error handling for invalid credentials
- Auto-redirect if already logged in

### Navigation
- Shows current logged-in user
- Logout functionality
- Admin panel access

### Protected Pages
- Dashboard
- Service Inward Management
- Customer Management
- Service Ledger
- Print Reports

## 🔄 Logout

- Click on the user dropdown in the top navigation
- Select "Logout"
- You'll be redirected to the login page

## 🚨 Troubleshooting

### If you can't log in:
1. Reset the admin password: `py manage.py reset_admin_password`
2. Try logging in with: username=`admin`, password=`admin123`

### If you get permission errors:
1. Make sure you're logged in as an admin user
2. Check if the user has proper permissions in the admin panel

### If the server won't start:
1. Check if the virtual environment is activated
2. Run: `py manage.py check` to identify issues
3. Make sure all migrations are applied: `py manage.py migrate`

## 📞 Support

For any issues with the authentication system, contact the system administrator. 