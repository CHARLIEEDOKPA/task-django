from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.models import User
import re


from myapp.forms import LoginForm, RegisterForm

# Create your views here.

def login(request:HttpRequest):
    if request.method == "GET":
        return render(request,"login.html",{
            "form":LoginForm()
      })
    else: 
        correo = request.POST["usuario"]
        password = request.POST["password"]
        user = authenticate(username=correo,password=password)
        
        if user is not None:
            return redirect('/tasks/login')
        else:
            messages.error(request,"Las credenciales están incorrectas")
            return redirect('/tasks/login')
        
        
def register(request:HttpRequest):
    if request.method == "GET":
        return render(request,"register.html",{
            "form": RegisterForm()
        })
    else:
        created_user,message = create_user(request.POST)
        if created_user is None:
            messages.error(request,message)
            return redirect("/tasks/register")
        return redirect("/tasks/login")
    
    
def create_user(data):
    password = data['password']
    username = data['username']  
    if user_exists(username):
        return None, "El usuario que has puesto ya existe"
    if not password_correct_formated(password):
        return None,"La contraseña tiene que tener como mínimo 6 carácteres"
        
    user = User.objects.create_user(username,data['email'],password)
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.save()
    
    return user,"El usuario ha sido creado correctamnete"
    
    

def password_correct_formated(password):
    pattern = r"[0-9a-zA-z]{6}"
    return re.match(pattern,password) is not None

def user_exists(usermame):
    return User.objects.get(username=usermame) is not None