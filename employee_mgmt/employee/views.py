from django.shortcuts import redirect, render ,get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Employee
from .forms import EmployeeForm , EmployeeCreateForm
from django.contrib.auth.models import User



# Create your views here.

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

def is_hr(user):
    return user.is_authenticated and user.role == 'hr'


def is_admin_or_hr(user):
    return user.is_authenticated and user.role in ['admin', 'hr']

@login_required
@user_passes_test(is_admin_or_hr)
def employee_list(request):
    employees = Employee.objects.all()
    return render(request , 'employee/employee_list.html', {'employees': employees})

@login_required
@user_passes_test(is_admin_or_hr)
def employee_detail(request,pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request,'employee/employee_detail.html',{'employee':employee})

@login_required
@user_passes_test(is_admin_or_hr)
def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_detail', pk=employee.pk)
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'employee/employee_edit.html', {'form': form, 'employee': employee})

@login_required
@user_passes_test(is_admin_or_hr)
def employee_add(request):
    form = EmployeeForm(request.POST or None , request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('employee_list')
    return render(request, 'employee/employee_form.html', {'form': form})

@login_required
@user_passes_test(is_admin_or_hr)
def employee_delete(request , pk):
    employee = get_object_or_404(Employee,pk = pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee_list')
    return render(request , 'employee/employee_confirm_delete.html',{'employee':employee})

@login_required
def my_profile(request):
    employee = get_object_or_404(Employee, user=request.user)
    return render(request, 'employee/my_profile.html', {'employee': employee})


def create_employee(request):
    if not request.user.is_authenticated or request.user.role not in ['admin', 'hr']:
        return redirect('login')

    if request.method == 'POST':
        form = EmployeeCreateForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            password = form.cleaned_data['password']
            return render(request, 'employee/employee_created.html', {
                'username': user.username,
                'password': password,
            })
    else:
        form = EmployeeCreateForm()
    return render(request, 'employee/employee_form.html', {'form': form})

