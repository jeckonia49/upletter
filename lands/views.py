from django.shortcuts import render
from django.views.generic import TemplateView, View
from posts.models import Post, Category, Genre, Video
from .mixins import HomeGridLandingMixin, HomeTopLandinMixin, PaginationMixin
from .forms import ContactForm, SubscriptionForm
from accounts.views import SuccessUrlRedirect
from django.contrib import messages
from .models import Subscription
from django.utils import timezone
from datetime import timedelta
# Create your views here.

class HomeLandinView(HomeGridLandingMixin, HomeTopLandinMixin, TemplateView):
    """The inheritance caries the post for the grids"""
    """This form of inheritance makes this code easi to read and undersatand"""
    template_name = "index.html"
    queryset = Post
    category=Category
    videos = Video

    def get_main_hero(self, **kwargs):
        """main hero slider"""
        return self.queryset.objects.all().order_by("-timestamp")
    
    def get_ajax_category(self, **kwargs):
        return self.category.objects.all().order_by("?")[:4]
    
    def get_recent_timing(self):
        return timezone.now()-timedelta(days=5)
    
    def get_popular_recent_videos(self):
        return self.videos.objects.filter(timestamp__gte=self.get_recent_timing()).all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        """The other grid posts are with tthe super dictionary"""
        context["main"] = self.get_main_hero(**kwargs)
        context['ajax'] = self.get_ajax_category(**kwargs)
        context['videos'] = self.get_popular_recent_videos()
        return context
    
class ContactUsView(SuccessUrlRedirect, View):
    form_class = ContactForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message saved successfully")
            return self.get_success_url(*args, **kwargs)
        messages.error(request, "Error sending the message. Retry!")
        return self.get_success_url(*args, **kwargs)
    
class SubscriptionView(SuccessUrlRedirect, View):
    form_class = SubscriptionForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            subscription, created = Subscription.objects.update_or_create(email=form.cleaned_data.get("email"))
            if created:
                messages.success(request, "Subscription saved")
                return self.get_success_url(*args, **kwargs)
            if subscription:
                messages.info(request, "You're already subscribed!")
                return self.get_success_url(*args, **kwargs)
        messages.error(request, "Error subscription")
        return self.get_success_url(*args, **kwargs)
    

def get_ajax_view(request, ajax_category_pk):
    """This function get the ajax"""
    return render(request, "home/ajax/ajax.html", {"ajax_category": Category.objects.get(pk=ajax_category_pk)})

