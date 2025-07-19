from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Task
from .forms import TaskForm, TaskStatusForm
from django.http import HttpResponseForbidden

# HR or Admin check
def is_hr_or_admin(user):
    return user.role in ['admin', 'hr']

# HR/Admin: View all tasks
@login_required
@user_passes_test(is_hr_or_admin)
def task_list(request):
    tasks = Task.objects.all().order_by('-assigned_date')
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

# HR/Admin: Assign a task
@login_required
@user_passes_test(is_hr_or_admin)
def assign_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/assign_task.html', {'form': form})


# Employee: View latest assigned task
@login_required
def my_latest_task(request):
    task = Task.objects.filter(employee=request.user).order_by('-assigned_date').first()
    return render(request, 'tasks/my_latest_task.html', {'task': task})

# Employee: Update task status
@login_required
def update_task_status(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.employee != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = TaskStatusForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('my_latest_task')
    else:
        form = TaskStatusForm(instance=task)
    return render(request, 'tasks/update_task_status.html', {'form': form})
