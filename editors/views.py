from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from posts.models import Post
from accounts.models import Profile
from lands.mixins import   PaginationMixin
from .mixins import ModifiedLoginRequiredMixin, HandleProfileObjectMixin
from accounts.forms import ProfileForm, SocialProfileForm, socialFormSet
from accounts.views import SuccessUrlRedirect
from django.http import HttpResponseRedirect

class EditorPublicView(PaginationMixin, TemplateView):
    queryset = Post
    profile = Profile
    context_object_name = "posts"
    paginate_by = 20
    template_name = "editors/posts.html"

    def get_profile(self, **kwargs):
        return get_object_or_404(self.profile, user__email=f"{kwargs.get('editor_username')}@gmail.com")
    
    def get_queryset_from_latest(self, **kwargs):
        return self.queryset.objects.filter(profile=self.get_profile(**kwargs)).order_by("-timestamp")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['editor'] = self.get_profile(**kwargs)
        return context




class EditorPrivateView(ModifiedLoginRequiredMixin, HandleProfileObjectMixin):
    """This is the main class to be passed on to the views"""
    template_name = "editors/profile/index.html"
    profile = Profile


class EditorUpdatePrivateView(ModifiedLoginRequiredMixin, HandleProfileObjectMixin, SuccessUrlRedirect):
    """This is the update view"""
    template_name = "editors/profile/update.html"
    profile = Profile
    form_class = ProfileForm
    formset = socialFormSet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.get_profile(**kwargs))
        context['formset'] = self.formset(self.request.GET)
        return context
    

    def post(self, *args, **kwargs):
        form = self.form_class(self.request.POST, self.request.FILES, instance=self.get_profile(**kwargs))
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user=self.request.user
            form.save()
            return self.get_success_url(*args, **kwargs)


class SocialFormCreateView(HandleProfileObjectMixin, SuccessUrlRedirect):
    template_name = "editors/profile/update.html"
    form_class = socialFormSet
    
    def post(self, request, *args, **kwargs):
        formset = self.form_class(request.POST)
        if formset.is_valid():
            for form in formset:
                print(form.cleaned_data)
            print(formset.cleaned_data)
        return self.get_success_url(*args, **kwargs)