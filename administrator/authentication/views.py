from django.views.generic import FormView, ListView, TemplateView, View
from accounts.forms import LoginModalForm
from accounts.models import MyUser, Profile
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages


class AdministratorLoginView(FormView):
    template_name = "administrator/authentication/login.html"
    form_class = LoginModalForm
    success_url=reverse_lazy("administrator:home")

    def form_valid(self, form):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            user=MyUser.objects.get(email=form.cleaned_data.get("email"))
            login(self.request, user)
            messages.success(self.request, "Loggin was successful")
            return redirect(self.success_url)
    