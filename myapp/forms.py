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