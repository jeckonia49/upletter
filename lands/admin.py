from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from lands.models import ContactFlatPage, Contact, SiteSocialLink, Subscription, TinymceApiKey,  ContactFlatPage, AboutFlatPage, Page404Error
from django.core.exceptions import ValidationError
# Define a new FlatPageAdmin

from posts.models import Post, Video


@admin.register(Contact)
class AdminContact(admin.ModelAdmin):
    list_display = ['name', 'email',]

@admin.register(AboutFlatPage)
class AboutFlatPageAdmin(admin.ModelAdmin):
    list_display = ['page', 'cover_image']

@admin.register(ContactFlatPage)
class ContactFlatPageAdmin(admin.ModelAdmin):
    list_display = ['address','cover_image', 'phone', 'mail']

@admin.register(Page404Error)
class AdminPage404Error(admin.ModelAdmin):
    # impementation similar to the about and contact
    list_display = ['page', 'cover_image']

@admin.register(SiteSocialLink)
class AdminSiteSocialLink(admin.ModelAdmin):
    list_display = ['name', 'link']
    list_display_links = ['name', 'link']

@admin.register(Subscription)
class AdminSubscription(admin.ModelAdmin):
    list_display = ['email', ]

@admin.register(TinymceApiKey)
class AdminTinymceApiKey(admin.ModelAdmin):
    list_display = ['key', ]

"""
CUSTOM DJANGO ADMIN PAGE INTERFACE

"""

class LandsCustomAdmin(admin.AdminSite):
    site_header = "Monty Gmag Administration"
    # this is a mini admin interface for the site writers
    # the writers have no access to the main admin interface
    
lands_admin_site = LandsCustomAdmin(name="myadmin")

class PostAdmin(admin.ModelAdmin):

    prepopulated_fields = {"slug": ("title",)}
    exclude = ("profile", )
    readonly_fields = ['comments',"views","editor_choice",]
    list_select_related = ['profile', 'category']
    list_display = [
        "profile","category","timestamp","updated_at","views",'comments',
    ]
    list_display_links = [
        "profile","category",
    ]
    list_filter = [
        "profile","category",
    ]
    search_fields = ['title']

    def save_model(self, request, obj, *args, **kwargs):
        obj.profile = request.user.user_profile
        obj.profile.save()
        obj.save()
        return super().save_model(request, obj, *args, **kwargs)
    
lands_admin_site.register(Post, PostAdmin)



class AdminVideo(admin.ModelAdmin):
    list_display = ["category","title","cover","url","timestamp"]
    prepopulated_fields = {"slug": ("title", )}
    search_fields = ['title']



lands_admin_site.register(Video, AdminVideo)
