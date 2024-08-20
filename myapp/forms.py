import datetime
from django import forms

class LoginForm(forms.Form):
    
    usuario = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
    
class RegisterForm(forms.Form):
    
    username = forms.CharField(max_length=100,min_length=4)
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField()
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=100)
    
class CreateTaskForm(forms.Form):
    title = forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.TextInput())
    due_time = forms.TimeField( initial=datetime.datetime.today(),
        widget=forms.TimeInput(attrs={'type': 'time'}))
    due_date = forms.DateField(initial=datetime.datetime.today(), widget=forms.DateInput(attrs={'type': 'date'}))
    