# payroll/admin.py
from django.contrib import admin
from .models import Payroll

@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = (
        'employee',
        'salary_month',
        'basic_salary',
        'bonus',
        'deductions',
        'net_salary',
    )

    list_filter = ('salary_month',)

    search_fields = (
        'employee__username',
        'employee__first_name',
        'employee__last_name',
    )

    readonly_fields = ('net_salary',)
