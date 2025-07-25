from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES=(
        ('admin','Admin'),
        ('hr','HR'),
        ('employee','Employee'),
    )
    # is_verified = models.BooleanField(default=False)
    # otp_code = models.CharField(max_length=6, blank=True, null=True)
    role = models.CharField(max_length=10,choices=ROLE_CHOICES)
    image= models.ImageField(upload_to='profile_pic/',default='default.png')

    def __str__(self):
         return f"{self.username}'s Profile"
