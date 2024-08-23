from django.urls import path

from myapp.views import create_task_view, dashboard, edit_task_view, login_view, logout_view,register,task_details_view,complete_task_view,not_complete_task_view,delete_task_view,task_list_view


urlpatterns = [
    path("login/", login_view,name="login"),
    path("register/", register,name="register"),
    path("dashboard/",dashboard,name="dashboard"),
    path("logout/",logout_view,name="logout"),
    path("create_task/",create_task_view,name="create_task"),
    path("<int:id>/",task_details_view,name="task_details"),
    path("completed/<int:id>",complete_task_view,name="completed",),
    path("not-completed/<int:id>",not_complete_task_view,name="not_completed"),
    path("delete/<int:id>",delete_task_view,name="delete"),
    path("list/",task_list_view,name="task_list"),
    path("edit/<int:id>", edit_task_view,name="edit_task")
]
