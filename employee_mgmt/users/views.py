from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomLoginForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from employee.models import Employee 
from employee.forms import EmployeeForm
# Create your views here.

from django.utils.timezone import now

def home_view(request):
    return render(request, 'home.html', {'now': now()})

def register_view(request):
    form = CustomUserCreationForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        user = form.save()
        if user.role == 'employee':
            Employee.objects.create(user=user,date_of_joining=now().date())
        login(request, user)
        return redirect('dashboard')  # Redirect to role-based dashboard
    else:
        print(form.errors)
    return render(request, 'users/register.html', {'form': form})

@login_required
def role_dashboard(request):
    if request.user.role == 'admin':
        return redirect('admin_dashboard')
    elif request.user.role == 'hr':
        return redirect('hr_dashboard')
    elif request.user.role == 'employee':
        return redirect('employee_dashboard')
    else:
        return HttpResponse("Role not defined.")
    
     



def login_view(request):
    form = CustomLoginForm(data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        
        # Redirect based on role
        if user.role == 'admin':
            return redirect('admin_dashboard')
        elif user.role == 'hr':
            return redirect('hr_dashboard')
        else:
            return redirect('employee_dashboard')
    return render(request, 'users/login.html', {'form': form})

    
def logout_view(request):
    logout(request)
    return redirect('login')  

def admin_dashboard(request):
    return render(request, 'users/admin_dashboard.html')

def hr_dashboard(request):
   return render(request, 'users/hr_dashboard.html')

def employee_dashboard(request):
   return render(request, 'users/employee_dashboard.html')
    



