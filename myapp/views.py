from django.http import HttpRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

from myapp.defs import create_user,check_date_and_time, is_logged, is_tarea_owner, return_date_time_from_post, toggle_complete_task, complete_a_task, collect_date_time_by_post, edit_tarea
from myapp.forms import CreateTaskForm, LoginForm, RegisterForm
from myapp.models import Tarea
import datetime

# Create your views here.

#Vista para rederigir al dashboard
def redirect_dashboard(request:HttpRequest):
    return redirect("dashboard")


#Vista para el login
def login_view(request:HttpRequest):
    if request.method == "GET":
        return render(request,"login.html",{
            "form":LoginForm()
      })
    else: 
        correo = request.POST["usuario"]
        password = request.POST["password"]
        user = authenticate(username=correo,password=password)
        
        if user is not None:
            login(request,user)
            return redirect("dashboard")
        else:
            messages.error(request,"Las credenciales están incorrectas")
            return redirect('login')
        
#Vista para registrar un usuario        
def register(request:HttpRequest):
    if request.method == "GET":
        return render(request,"register.html",{
            "form": RegisterForm()
        })
    else:
        created_user,message = create_user(request.POST)
        if created_user is None:
            messages.error(request,message)
            return redirect("register")
        return redirect("login")
    

#Vista para la pagina principal del usuario que seria el dashboard  
def dashboard(request:HttpRequest):
    if not is_logged(request): 
        return redirect("login")
    
    user_id = request.user.id
    tareas = Tarea.objects.all().filter(user_id = user_id)
    priority = request.GET.get("priority")
    
    if priority != None and priority != "none":
        print("Entra")
        tareas = tareas.filter(priority = priority)
    
        
    return render(request,"dashboard.html",{
        "tareas": tareas,
        "todays_datetime": datetime.datetime.today(),
        "todays_date":datetime.date.today()
    })
        
        
#Vista que cierra sesión    
def logout_view(request:HttpRequest):
    logout(request)
    return redirect("login")



#Vista para crear una tarea
def create_task_view(request:HttpRequest):
    if not is_logged(request):
        return redirect("login")

    if request.method == "GET":
        return render(request,"create_task.html",{
            "form": CreateTaskForm()
        })
    else:
        
        data = request.POST
        user = request.user
        
        due_date, due_time = collect_date_time_by_post(data)
        
        
        datetime_user = return_date_time_from_post(due_date, due_time)
        correct_datetime = check_date_and_time(datetime_user)
        
        if correct_datetime:
            Tarea.objects.create(title=data["title"],description=data["description"],user_id=user.id,priority=data["priority"]
                                 ,due_date=datetime_user)
            return redirect("dashboard")
            
        messages.error(request,"La fecha que pusiste ya ha pasado")   
        return redirect("create_task")
    

#Vista para ver el detalle de una tarea    
def task_details_view(request:HttpRequest, id):
    
    if not is_logged(request):
        return redirect("login")
    
    tarea = get_object_or_404(Tarea,id=id)
    
    user = request.user
    
    if tarea.user != user:
        return redirect("dashboard")
    
    return render(request,"task-details.html",{
        "tarea":tarea
    })
    
    
 #Vista para completar una tarea   
def complete_task_view(request:HttpRequest, id):
    if not is_logged(request):
        return redirect("login")
    return complete_a_task(request,id,complete=True)

#Vista para no completar una tarea que antes estaba completada
def not_complete_task_view(request:HttpRequest,id):
    if not is_logged(request):
       return redirect("login")
    return complete_a_task(request,id,complete=False)
   

#Vista para borrar una tarea
def delete_task_view(request:HttpRequest,id):
    
    if not is_logged(request):
       return redirect("login")
    
    tarea = get_object_or_404(Tarea, id=id)
    
    if not is_tarea_owner(tarea,request):
         return redirect("dashboard")
    
    if request.method == "GET":
        return render(request,"confirm-delete.html", {
            "tarea":tarea
        })
    else:
        tarea.delete()
        return redirect("dashboard")
    
    
#Vista para la lista de tareas        
def task_list_view(request:HttpRequest):
    if not is_logged(request):
       return redirect("login")
   
    user_id = request.user.id
    tareas = Tarea.objects.all().filter(user_id = user_id)
    
    if len(tareas) == 0:
        return redirect("dashboard")
    
    return render(request,"tasks-list.html", {
        "tareas":tareas
    })
    

#Vista para editar una tarea    
def edit_task_view(request:HttpRequest, id): 
    if not is_logged(request):
        return redirect("login")
        
    tarea = get_object_or_404(Tarea, id=id)
    
    if not is_tarea_owner(tarea,request):
        return redirect("task_list")
    
    if request.method == "GET":  
        title = tarea.title
        form =  CreateTaskForm(initial={"title":title,
                                        "description":tarea.description,
                                        "priority":tarea.priority,
                                        "due_date":tarea.due_date.date,
                                        "due_time": tarea.due_date.time})
        return render(request,"edit-task.html",{
            "form":form,
            "title":title
        })
    
    else:
        data = request.POST
        due_date, due_time = collect_date_time_by_post(data)
        
        datetime_user = return_date_time_from_post(due_date, due_time)
        correct_datetime = check_date_and_time(datetime_user)
        
        if not correct_datetime:
           messages.error(request,"La fecha que pusiste ya ha pasado") 
           return redirect(f"/tasks/edit/{id}")
       
        edit_tarea(tarea,data,datetime_user)
        return redirect("task_list")
    
    

    
    
    
