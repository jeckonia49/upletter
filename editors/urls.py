from django.urls import path
from . import views

app_name = "editors"

urlpatterns = [
    path("", views.EditorPrivateView.as_view(), name="profile"),
    path("<post_slug>/", views.EditorPrivateDeletePostView.as_view(), name="post_delete_view"),
    path("profile/update/", views.EditorUpdatePrivateView.as_view(), name="update"),
    path("profile/update/social/", views.SocialFormCreateView.as_view(), name="update-social"),
    path("<editor_username>/", views.EditorPublicView.as_view(), name="editor_view"),
]
