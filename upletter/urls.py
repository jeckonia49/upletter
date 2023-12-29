from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.flatpages import views as flatpages_views
from lands.admin import lands_admin_site
from . import views


urlpatterns = [
    path("super-admin-login/", admin.site.urls),
    path("editor-admin-login/", lands_admin_site.urls),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path('tinymce/', include('tinymce.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path("", include("lands.urls")),
    path("posts/", include("posts.urls", namespace="posts")),
    path("editors/", include("editors.urls", namespace="editors")),
    path("shops/", include("shop.urls", namespace="shops")),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# path for flatpages urls
# will append the not found page here
urlpatterns += [
    path('about-us/', flatpages_views.flatpage, {'url': '/about-us/',} , name='about'),
    path('contact-us/', flatpages_views.flatpage, {'url': '/contact-us/',} , name='contact'),
    path('not-found/', flatpages_views.flatpage, {'url': '/not-found/',} , name='not-found'),
    path('license/', flatpages_views.flatpage, {'url': '/license/'}, name='license'),
]



admin.AdminSite.site_header = "GMAG Administration"
admin.AdminSite.site_title = "Gmag Website"


handler404="upletter.handlers.handler404"
handler500="upletter.handlers.handler500"
