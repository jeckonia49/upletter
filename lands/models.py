from django.contrib.flatpages.models import FlatPage
from django.db import models


class TinymceApiKey(models.Model):
    # THhis is the model for the tinymce key editor
    key = models.CharField(max_length=1000)
    def __str__(self):
        return self.key
    
    @classmethod
    def object(cls):
        return cls._default_manager.all().first()
    
    def save(self, *args, **kwargs):
        # this ensure only one object can be saved in the database at a got and replaces the exixting 
        #  one with the new creation so that at no givent tine will there be more than one key
        self.pk = self.id = 1
        return super().save(*args, **kwargs)
    

class AboutFlatPage(models.Model):
    page=models.OneToOneField(FlatPage, on_delete=models.CASCADE, related_name="about_flatepage")
    cover_image = models.ImageField(upload_to="flatpages/contact/", blank=True, null=True)
    message = models.TextField(max_length=1000, default="Your website is fully responsive so visitors can view your content from their choice of device.")

    class Meta:
        verbose_name = "About FlatPage"
        verbose_name_plural = "About FlatPages"


class ContactFlatPage(models.Model):
    page=models.OneToOneField(FlatPage, on_delete=models.CASCADE, related_name="contact_flatepage")
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, help_text="phone number startting with the country code i.e 2447(123)987654")
    mail = models.EmailField(max_length=255, help_text="gmagnews@domain.com")
    cover_image = models.ImageField(upload_to="flatpages/contact/", blank=True, null=True)


    class Meta:
        verbose_name = "Contact FlatPage"
        verbose_name_plural = "Contact FlatPages"

class ItemThreeAbstractModel(models.Model):
    """Becase the comment and the contact model have the same fields: we use this holder for these field"""
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # These models will holder these 4 field wich are being sahred with some models below
    # the model is then passed as a abstract for inheritance

    class Meta:
        abstract=True
        ordering = ['name']

    def __str__(self):
        
        return self.name

class Contact(ItemThreeAbstractModel):
    # contact uses the fields and been that those are what are needed
    # there is no need for defining any field
    
    pass

class SocialIcon(models.TextChoices):
    IG = "IG", "fa-instagram"
    FB = "FB", "fa-facebook-f"
    PT = "PIN", 'fa-pinterest-p'

class SiteSocialLink(models.Model):
    name = models.CharField(max_length=100, unique=True)
    link = models.URLField(max_length=255)
    icon = models.CharField(max_length=3, choices=SocialIcon.choices)

    def __str__(self):
        return self.name
    
class Subscription(models.Model):
    email = models.EmailField(max_length=100)

    def __str__(self):
        return self.email

class Page404Error(models.Model):
    """Create a single custom 404 page based on the flat pages to prevent multiple creation of the model"""
    # imlemenetation similar as the about and contact use page
    page=models.OneToOneField(FlatPage, on_delete=models.CASCADE, related_name="error_flatepage")
    cover_image = models.ImageField(upload_to="404/")

    def __str__(self):
        return f"404 Page"
    
