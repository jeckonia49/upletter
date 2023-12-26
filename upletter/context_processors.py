from accounts.forms import LoginModalForm, RegisterModalForm
from posts.models import Category, Tag, Post
from django.utils import timezone
from datetime import timedelta
from lands.models import SiteSocialLink, TinymceApiKey
from lands.forms import  SubscriptionForm

def filter_time():
    return timezone.now() + timedelta(days=3)

def site_context_processor_data(request):
    return dict(
        rform=RegisterModalForm(),
        lform=LoginModalForm(),
        footer_categories = Category.objects.all().order_by("-id")[:6],
        popular=Post.objects.filter(views__gte=1000).all().order_by("-timestamp")[:5],
        recent=Post.objects.filter(timestamp__lte=filter_time()).all().order_by("-timestamp")[:5],
        editor=Post.objects.filter(editor_choice=True).all().order_by("-timestamp"),
        tags = Tag.objects.all()[:9],
        site_social=SiteSocialLink.objects.all()[:5],
        subscription_form=SubscriptionForm(),
        tinymce_api_key=TinymceApiKey.object,
    )

