from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect


class ModifiedLoginRequiredMixin(LoginRequiredMixin):
    """This inheritance will allow modification of the further class coc
        ill be using is here alot
        """
    login_url = reverse_lazy(settings.LOGIN_URL)

    def dispatch(self, request, *args, **kwargs):
        """This is the class for the redirect"""
        if not request.user.is_authenticated:
            messages.warning(request, "You have no permission to access this page")
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)
    
class HandleProfileObjectMixin(TemplateView):
    template_name = ""
    profile = None
    
    def get_profile(self, **kwargs):
        return get_object_or_404(self.profile, user__email=self.request.user.email)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['editor'] = self.get_profile(**kwargs)
        return context

