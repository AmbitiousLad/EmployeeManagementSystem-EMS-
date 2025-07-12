from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Payroll
from .forms import PayrollForm
from django.conf import settings
import os
from django.http import HttpResponseForbidden
from django.http import HttpResponse


# Create your views here.

def is_admin_or_hr(user):
    return user.role == 'admin' or user.role == 'hr'


@login_required
@user_passes_test(is_admin_or_hr)
def payroll_list(request):
    payrolls = Payroll.objects.all().order_by('-salary_month')
    return render(request,'payroll/payroll_list.html',{'payrolls':payrolls})


@login_required
@user_passes_test(is_admin_or_hr)
def payroll_create(request):
    if request.method == 'POST':
        form = PayrollForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payroll_list')
    else:
        form = PayrollForm()
    return render(request , 'payroll/payroll_form.html',{'form':form})

@login_required
def my_payslips(request):
    payrolls = Payroll.objects.filter(employee=request.user).order_by('-salary_month')
    return render(request, 'payroll/my_payslips.html', {'payrolls': payrolls})   


@login_required
def payroll_detail(request, pk):
    payroll = get_object_or_404(Payroll, pk=pk)
    # Security: Only allow employee to view their own payroll or HR/Admin
    if request.user != payroll.employee and request.user.role not in ['admin', 'hr']:
        return HttpResponseForbidden()
    return render(request, 'payroll/payroll_detail.html', {'payroll': payroll})

# @login_required
# def payroll_detail(request):
#     payroll = Payroll.objects.filter(employee=request.user).order_by('-salary_month').first()

#     if not payroll:
#         return HttpResponse("No payroll record found for you.", status=404)

#     return render(request, 'payroll/payroll_detail.html', {'payroll': payroll})
