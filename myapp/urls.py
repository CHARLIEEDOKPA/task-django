from django.urls import path

from myapp.views import login, register


urlpatterns = [
    path("login/", login),
    path("register/", register,name="register")
]
