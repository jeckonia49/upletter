from posts.models import Tag, Post
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
from .models import Category

def filter_time():
    return timezone.now() + timedelta(days=3)

def post_context_processor_data(request):
    """This ensure that we can be able to access the database item even in place where we cant 
    grab then from the views, for example the cart items which is in the navbar, need to be kept tracj of
    Also the popula and recent posts whihc are been passed onto dir=fferent pages
    including the footer links(the footer beebg sahred onto the entire site so the content also need to be 
    consistent)"""
    # each app has its own 
    # for cleanliness
    return dict(
        popular=Post.objects.filter(views__gte=1000).all().order_by("-timestamp")[:5],
        recent=Post.objects.filter(timestamp__lte=filter_time()).all().order_by("-timestamp")[:5],
        editor=Post.objects.filter(editor_choice=True).all().order_by("-timestamp"),
        tags = Tag.objects.all()[:9],
        aside_category=Category.objects.filter(icon__isnull=False).all()[:6]
    )

