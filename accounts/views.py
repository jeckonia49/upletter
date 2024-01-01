from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View, ListView, DetailView, FormView
from .forms import LoginModalForm, RegisterModalForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import MyUser

class SuccessUrlRedirect:
    def get_success_url(self, *args, **kwargs):
        return HttpResponseRedirect(self.request.META.get("HTTP_REFERER"))

class LoginView(View,SuccessUrlRedirect):
    form_class = LoginModalForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_email(), password=form.cleaned_password())
            if user is not None:
                login(request, user)
                messages.success(request, "Your Login was Successful ")
                return self.get_success_url(*args, **kwargs)
        messages.error(request, "Invalid user credetials")
        return self.get_success_url(*args, **kwargs)

class LogoutView(View,SuccessUrlRedirect):
    def post(self, request, *args, **kwargs):
        logout(request)
        return self.get_success_url(*args, **kwargs)

class SignUpView(View,SuccessUrlRedirect):
    form_class = RegisterModalForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = MyUser.objects.filter(email=form.cleaned_email()).exists()
            if user:
                messages.error(request, "User with that email already exists!")
                return self.get_success_url(*args, **kwargs)
            else:
                form.save()
                messages.success(request, "Account creation sucessful!")
                # proceed to login the user
                active_user = authenticate(request, username=form.cleaned_email(), password=form.clean_password2())
                login(request, active_user)
                return self.get_success_url(*args, **kwargs)
        messages.error(request, "Invalid user credetials")
        return self.get_success_url(*args, **kwargs)
