from django.db import models
from django.conf import settings
# Create your models here.

class Leave(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('sick', 'Sick Leave'),
        ('casual', 'Casual Leave'),
        ('earned', 'Earned Leave'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    employee = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)
    leave_type = models.CharField(max_length=20,choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
    reason = models.TextField()
    applied_on = models.DateTimeField(auto_now_add=True)
     
    def __str__(self):
        return f"{self.employee.username} - {self.leave_type} ({self.status})"