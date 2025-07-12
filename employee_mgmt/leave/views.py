from django.shortcuts import render
from django.contrib.auth.decorators import login_required , user_passes_test
from .forms import LeaveForm
from .models import Leave
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
# Create your views here.


def is_hr_or_admin(user):
    return user.is_authenticated and (user.role == 'hr' or user.role == 'admin')

@login_required
def leave_apply(request):
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = request.user
            leave.save()
            return redirect('leave_list')
    else:
        form = LeaveForm()
    return render(request, 'leave/apply_leave.html', {'form': form})        

@login_required
def leave_list(request):
    leaves = Leave.objects.filter(employee=request.user).order_by('-applied_on')
    return render(request, 'leave/leave_list.html', {'leaves': leaves})



@login_required
@user_passes_test(is_hr_or_admin)
def leave_manage(request):
    leaves = Leave.objects.all().order_by('-applied_on')
    return render(request, 'leave/manage_leaves.html', {'leaves': leaves})

@login_required
@user_passes_test(is_hr_or_admin)
def approve_leave(request,pk):
    leave = get_object_or_404(Leave,pk=pk)
    leave.status = 'approved'
    leave.save()
    return redirect('manage_leaves')

@login_required
@user_passes_test(is_hr_or_admin)
def reject_leave(request,pk):
    leave = get_object_or_404(Leave,pk=pk)
    leave.status = 'rejected'
    leave.save()
    return redirect('manage_leaves')
