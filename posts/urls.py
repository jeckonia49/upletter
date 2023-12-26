from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path("", views.PostListView.as_view(), name="posts"),
    path("<post_slug>/", views.PostDetailView.as_view(), name="post_detail"),
    path("search/posts/", views.PostListSearchView.as_view(), name="post_search"),
    path("<post_slug>/post/comment/", views.PostDetailCommentCreateView.as_view(), name="post_comment"),
    path("category/<category_slug>/", views.CategoryPostListView.as_view(), name="category_detail"),
]

