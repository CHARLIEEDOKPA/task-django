import re
from django.contrib.auth.models import User
import datetime

from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect

from myapp.models import Tarea

#Esta funcion crea el usuario y lo que devuelve es una tupla
def create_user(data):
    password = data['password']
    username = data['username'] 
    
    #Si el usuario existe o que la contraseña no es la que pide(6 caracteres como mínimo)
    # ,se enviara una tupla con un mensaje de error y un None 
    
    if user_exists(username):
        return None, "El usuario que has puesto ya existe"
    if not password_correct_formatted(password):
        return None,"La contraseña tiene que tener como mínimo 6 caracteres"
     
    #Si todo va biense creará el usuario y retornara la tupla con el usuario creado y un mensaje
    #de que todo va bien
    
    user = User.objects.create_user(username,data['email'],password)
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.save()
    
    return user,"El usuario ha sido creado correctamente"
    
    
#Esta función comprueba si la contraseña que pasa en el parámetro tiene al menos 6 caracteres
def password_correct_formatted(password):
    pattern = r"[0-9a-zA-z]{6}"
    return re.match(pattern,password) is not None

#Función que comprueba si el usuario existe, retorna valor booleano
def user_exists(username):
    existed_user = User.objects.all().filter(username=username).first()
    return existed_user is not None

#Comprueba si ese dia que ha posado el usuario ya ha pasado, retorna valor booleano
def check_date_and_time(datetime_user:datetime.datetime):
    current_date = datetime.datetime.today()
    return datetime_user > current_date
 

#Lo que hace es pasar un array de strings a un array de integers, retorna un array de integers
def str_list_to_int_list(arr):
    return list(map(lambda x: int(x), arr))

#La función devolverá un datetime pasado el usuario
def return_date_time_from_post(date, time):
    date_splitted = date.split("-")
    time_splitted = time.split(":")
    
    year,month,day = tuple(str_list_to_int_list(date_splitted))

    hour,minute = tuple(str_list_to_int_list(time_splitted))
    
    
    
    return datetime.datetime(year,month,day,hour,minute)


#Comprueba si sigue autenticado el programa
def is_logged(request:HttpRequest):
    return request.user.is_authenticated
  
    
#Lo que hace es completar una tarea,por defecto el completed esta falso es decir, que
#si el llama esta función sin poner el parámetro completed en True, sería una tarea no completa 
#y si fuese al revés, estaría completo
    
def toggle_complete_task(request:HttpRequest,id,completed=False):
    tarea = get_object_or_404(Tarea,id=id)
    user = request.user
    
    if tarea.user == user:  
        tarea.completed = completed
        tarea.save()
        
        
#Comprueba si el usuario es el propietario de esa tarea      
def is_tarea_owner(tarea:Tarea,request:HttpRequest):
    return tarea.user == request.user

#Esa función devuelve datetime a segundos
def get_epoch_milliseconds(date:datetime.datetime): 
    return date.now().timestamp() * 1000

#Esa función completa o no completa una tarea depende del parámetro "complete"
def complete_a_task(request:HttpRequest,id, complete=False):
    if request.method == "POST":
        toggle_complete_task(request,id,completed=complete)
        if request.POST.get("task_list") != None:
            return redirect("task_list")
    return redirect("dashboard")

#Esta funciona devolverá una tupla con los valores de date y time
def collect_date_time_by_post(data):
    return data["due_date"], data["due_time"]


#Función para editar una tarea
def edit_tarea(tarea:Tarea,data,due_date:datetime.datetime):
    tarea.title = data["title"]
    tarea.description = data["description"]
    tarea.priority = data["priority"]
    tarea.due_date = due_date
    tarea.save()