from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.AdministratorLoginView.as_view(), name="login"),
]
