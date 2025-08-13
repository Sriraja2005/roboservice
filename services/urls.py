from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Service Inward Management
    path('inward/', views.service_inward_list, name='service_inward_list'),
    path('inward/add/', views.add_service_inward, name='add_service_inward'),
    path('inward/<int:service_id>/edit/', views.edit_service, name='edit_service'),
    path('inward/<int:service_id>/status/', views.update_service_status, name='update_service_status'),
    
    # Service Ledger
    path('ledger/', views.service_ledger, name='service_ledger'),
    path('ledger/<int:service_id>/', views.service_ledger, name='service_ledger_detail'),
    path('ledger/<int:service_id>/add-entry/', views.add_ledger_entry, name='add_ledger_entry'),
    path('ledger/<int:service_id>/add-expense/', views.add_expense, name='add_expense'),
    
    # Customer Management
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/<int:customer_id>/', views.customer_detail, name='customer_detail'),
    
    # Print Reports
    path('print/<int:service_id>/', views.print_service_report, name='print_service_report'),
] 