from django.shortcuts import render
from django.contrib.auth.decorators import login_required,user_passes_test
from .models import Attendance
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.utils.timezone import now


# Create your views here.


def admin_or_hr(user):
    return user.is_authenticated and (user.role == 'admin' or user.role == 'hr')


@login_required
def attendance_list(request):
    attendance_list = Attendance.objects.filter(employee=request.user).order_by('-date')
    return render(request,'attendance/attendance_list.html', {'attendance_list': attendance_list})


@login_required
def mark_attendance(request):
    today = timezone.now().date()
    attendance , created = Attendance.objects.get_or_create(employee=request.user,date=today)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'check_in' and not attendance.check_in_time:
            attendance.check_in_time = timezone.now()
            attendance.status = 'present'
            attendance.save()
        elif action == 'check_out' and attendance.check_in_time and not attendance.check_out_time:
            attendance.check_out_time = timezone.now()
            attendance.save()    

        return redirect('attendance_list')
    return render(request , 'attendance/mark_attendance.html',{'attendance' : attendance})   


@login_required
@user_passes_test(admin_or_hr)
def all_attendance(request):
    User = get_user_model()
    today = now().date()

    all_users = User.objects.all()
    attendance_records = Attendance.objects.filter(date=today)

    attendance_list = []

    for user in all_users:
        # Try to find this user's attendance record
        att = attendance_records.filter(employee=user).first()

        if att:
            attendance_list.append(att)
        else:
            attendance_list.append({
                'employee': user,
                'date': today,
                'check_in_time': None,
                'check_out_time': None,
                'status': 'absent'
            })

    return render(request, 'attendance/all_attendance.html', {
        'attendance_list': attendance_list,
        'today': today
    })

