# Generated by Django 5.2.4 on 2025-07-19 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='otp_code',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
