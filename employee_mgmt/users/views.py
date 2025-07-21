from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomLoginForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import CustomUser
import random
# Create your views here.

from django.utils.timezone import now

def home_view(request):
    return render(request, 'home.html', {'now': now()})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            otp = str(random.randint(100000, 999999))
            user.otp_code = otp
            user.is_active = False  # prevent login before verification
            user.save()

            send_mail(
                subject='Your OTP Code',
                message=f'Your verification code is {otp}',
                from_email='noreply@example.com',
                recipient_list=[user.email],
            )

            request.session['email'] = user.email
            return redirect('verify_otp')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def verify_otp(request):
    email = request.session.get('email')
    user = CustomUser.objects.filter(email=email).first()

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        if user and user.otp_code == entered_otp:
            user.is_verified = True
            user.is_active = True
            user.otp_code = ''
            user.save()

            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'users/verify_otp.html', {'error': 'Invalid OTP'})

    return render(request, 'users/verify_otp.html')

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
    



