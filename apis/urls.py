from django.urls import path, include
from apis.posts import urls as post_urls


urlpatterns = [
    path("", include("apis.posts.urls")),
]
