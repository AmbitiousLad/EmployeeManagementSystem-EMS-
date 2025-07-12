from django.urls import path
from . import views

urlpatterns = [
    path('', views.payroll_list, name='payroll_list'),
    path('create/', views.payroll_create, name='payroll_create'),
    path('mine/', views.my_payslips, name='my_payslips'),
    path('<int:pk>/', views.payroll_detail, name='payroll_detail'),
]
