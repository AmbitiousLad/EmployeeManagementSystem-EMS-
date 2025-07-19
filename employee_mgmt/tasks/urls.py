from django.urls import path
from . import views

urlpatterns = [
    path('assign/', views.assign_task, name='assign_task'),
    path('all/', views.task_list, name='task_list'),
    path('my/', views.my_latest_task, name='my_latest_task'),
    path('update/<int:pk>/', views.update_task_status, name='update_task_status'),
]
