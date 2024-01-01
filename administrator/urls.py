from django.urls import path, include
from . import views, sessions


app_name="administrator"

urlpatterns = [
    path("", views.AdministratorView.as_view(), name="home"),
    path("profile/", views.AdministratorProfileView.as_view(), name="profile"),
    path("<int:pk>/", sessions.get_administrator_has_viewed_latest_post, name="test_cookie"),
    path("post/comment/<str:post_slug>/", views.get_post_comment_view, name="post_comment_view"),
    path("update/", views.get_update_administrator_view, name="update_administrator_view"),
    path("", include("administrator.authentication.urls")),
]
