from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),  
    path('register/', views.register_view, name='register'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),  
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.role_dashboard, name='dashboard'),
    path('adm/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('hr/dashboard/', views.hr_dashboard, name='hr_dashboard'),
    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),
]
