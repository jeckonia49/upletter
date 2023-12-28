from accounts.forms import LoginModalForm, RegisterModalForm
from posts.models import Category
from django.db.models import Q
from lands.models import SiteSocialLink, TinymceApiKey
from lands.forms import  SubscriptionForm
from shop.models import Product

def site_context_processor_data(request):
    return dict(
        rform=RegisterModalForm(),
        lform=LoginModalForm(),
        footer_categories = Category.objects.all().order_by("-id")[:6],
        header_categories = Category.objects.all().order_by("?")[:3],
        site_social=SiteSocialLink.objects.all()[:5],
        subscription_form=SubscriptionForm(),
        tinymce_api_key=TinymceApiKey.object,
        popular_product=Product.objects.filter(reviews__gte=200).all()
    )

