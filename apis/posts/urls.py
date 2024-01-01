from django.urls import path
from . import views


urlpatterns = [
    path("", views.PostApiListCreateView.as_view()),
    path("<slug>/", views.PostRetrieveUpdateDestroyAPIView.as_view())
]
