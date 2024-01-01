from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, TemplateView, View, FormView
from posts.models import Post, Category, Tag
from posts.forms import *
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.conf import settings
from accounts.models import MyUser, Profile
from accounts.views import SuccessUrlRedirect
from accounts.forms import *
from shop.models import Shop
from editors.mixins import *
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth import get_user
from .models import *
# Create your views here.


class AdministratorProfile(SingleObjectMixin):
    model = Profile
    object=None

    def get_context_data(self, **kwargs):
        context = super(AdministratorProfile, self).get_context_data(**kwargs)
        context['profile'] = self.get_object()
        return context
    
    def get_object(self):
        # this will be our profile
        return get_user(self.request).user_profile


class AdministratorView(ModifiedLoginRequiredMixin, ListView):
    """By importing the ModifiedLoginRequiredMixin """
    """"W e now do not need the the dispathc"""
    queryset=Post.objects.all()
    template_name="administrator/index.html"
    context_object_name = "posts"
    administrator_login_url=reverse_lazy(settings.ADMINISTRATOR_LOGIN_URL)
    shops = Shop
    users=MyUser
    # the login_url is what is redirected 
    # its set to home by default so that we have no error
    login_url = administrator_login_url

    
    def get_active_users(self):
        # get all users
        return self.users.objects.filter(is_active=True).all()
    
    def get_all_shops(self):
        return self.shops.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = self.get_active_users()
        context['shops'] = self.get_all_shops()
        return context

class AdministratorProfileView(
    AdministratorProfile, ModifiedLoginRequiredMixin, 
    ListView, SuccessUrlRedirect
    ):
    template_name="administrator/profile/profile.html"
    model = Post
    posts_session_data=AdministratorPostSession
    form_class = PostCommentForm
    administrator_update_form = ProfileForm
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        # this context will be implemented ater
        context = super().get_context_data(**kwargs)
        context['administrator_update_form'] = self.administrator_update_form()
        return context
    
    def get_post_object(self, **kwargs):
        """This method gets the current item(post)"""
        return get_object_or_404(self.queryset, slug=kwargs.get("post_slug"))    

    def get_administrator_session_view(self):
        pass



def get_post_comment_view(request, post_slug):
    if request.method=="POST":
        post = Post.objects.get(slug=post_slug)
        comment, response = PostComment.objects.update_or_create(
            post=post,
            name=get_user(request).user_profile.get_full_name(),
            email=get_user(request).email,
            message=request.POST.get("post_comment")
        )
        messages.success(request, "Comment posted successfully")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def get_update_administrator_view(request):
    profile_form = ProfileForm
    if request.method == "POST":
        post_data = request.POST
        profile_data = Profile.objects.update_or_create(
            user=get_user(request),
            first_name=profile_data['first_name'],
            last_name=profile_data['last_name'],
            skills=profile_data['skills'],
            bio=profile_data['bio'],
        )
        messages.success(request, "Comment posted successfully")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


    

