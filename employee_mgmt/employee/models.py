from django.db import models
from users.models import CustomUser
from django.utils.timezone import now

class Employee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
    department = models.CharField(max_length=100, default="General")
    designation = models.CharField(max_length=100, default="Employee")
    date_of_joining = models.DateField(default=now)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    phone = models.CharField(max_length=15, default="0000000000")
    address = models.TextField(default="Not Provided")

    def __str__(self):
        return f"{self.user.username} - {self.designation} in {self.department}"
