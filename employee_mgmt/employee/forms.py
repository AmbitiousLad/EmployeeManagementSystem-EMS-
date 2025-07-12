from django import forms
from .models import Employee
from users.models import CustomUser


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['user', 'department', 'designation', 'date_of_joining', 'salary', 'phone', 'address']
        widgets = {
            'date_of_joining': forms.DateInput(attrs={'type': 'date'}),
        }

class EmployeeCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'image']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.role = 'employee'
        if commit:
            user.save()
        return user       