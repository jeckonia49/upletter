from django.urls import path
from . import views


urlpatterns = [
    path("", views.HomeLandinView.as_view(), name="home"),
    path("contact/send/", views.ContactUsView.as_view(), name="contact-send"),
    path("subscription/send/", views.SubscriptionView.as_view(), name="subscription"),
]
