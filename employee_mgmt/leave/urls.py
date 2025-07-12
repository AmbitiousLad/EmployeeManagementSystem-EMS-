from django.urls import path
from . import views

urlpatterns = [
    path('apply/', views.leave_apply, name='apply_leave'),
    path('my-leaves/', views.leave_list, name='leave_list'),
    path('manage/', views.leave_manage, name='manage_leaves'),
    path('approve/<int:pk>/', views.approve_leave, name='approve_leave'),
    path('reject/<int:pk>/', views.reject_leave, name='reject_leave'),
]
