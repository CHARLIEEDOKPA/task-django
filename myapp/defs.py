import re
from django.contrib.auth.models import User
import datetime

from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from myapp.models import Tarea

def create_user(data):
    password = data['password']
    username = data['username']  
    if user_exists(username):
        return None, "El usuario que has puesto ya existe"
    if not password_correct_formatted(password):
        return None,"La contraseña tiene que tener como mínimo 6 caracteres"
        
    user = User.objects.create_user(username,data['email'],password)
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.save()
    
    return user,"El usuario ha sido creado correctamente"
    
    

def password_correct_formatted(password):
    pattern = r"[0-9a-zA-z]{6}"
    return re.match(pattern,password) is not None

def user_exists(username):
    existed_user = User.objects.all().filter(username=username).first()
    return existed_user is not None


def check_date_and_time(datetime_user:datetime.datetime):
    current_date = datetime.datetime.today()
    return datetime_user > current_date
 


def str_list_to_int_list(arr):
    return list(map(lambda x: int(x), arr))


def return_date_time_from_post(date, time):
    date_splitted = date.split("-")
    time_splitted = time.split(":")
    
    year,month,day = tuple(str_list_to_int_list(date_splitted))
    hour,minute,second = tuple(str_list_to_int_list(time_splitted))
    
    return datetime.datetime(year,month,day,hour,minute,second)

def is_logged(request:HttpRequest):
    return request.user.is_authenticated
    
    
def toggle_complete_task(request:HttpRequest,id,completed=False):
    tarea = get_object_or_404(Tarea,id=id)
    user = request.user
    
    if tarea.user == user:  
        tarea.completed = completed
        tarea.save()
        
def is_tarea_owner(tarea:Tarea,request:HttpRequest):
    return tarea.user == request.user


def get_epoch_milliseconds(date:datetime.datetime): 
    return date.now().timestamp() * 1000