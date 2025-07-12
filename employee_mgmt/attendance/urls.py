from django.urls import path
from . import views

urlpatterns = [
    path('', views.attendance_list, name='attendance_list'),  # For employee's own attendance
    path('mark/', views.mark_attendance, name='mark_attendance'),  # For marking attendance
    path('all/', views.all_attendance, name='all_attendance'),  # For admin/hr to view all records
]
