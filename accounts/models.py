from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse
from django.db.models import Avg, Sum


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_editor = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Profile(models.Model):
    user = models.OneToOneField(
        MyUser, on_delete=models.CASCADE, related_name="user_profile"
    )
    profile_image = models.ImageField(
        upload_to="profile/images/", blank=True, null=True
    )
    cover_image = models.ImageField(upload_to="cover/images/", blank=True, null=True)
    bio = models.TextField(max_length=5000)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    skills = models.CharField(max_length=300, blank=True, null=True, help_text="if multiple skills, separate with commas")

    def __str__(self):
        return self.user.email
    
    def get_username(self):
        return f"{self.user.email[:self.user.email.index('@')]}"
    
    def get_full_name(self):
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}"
        else: return self.get_username()

    def get_profile_posts(self):
        return self.post_profile.all()
    
    def get_profile_post_views(self):
        return self.post_profile.aggregate(Sum("views"))['views__sum']

    def get_absolute_url(self):
        return reverse("editors:editor_view", kwargs={"editor_username": self.get_username()})
    
    def get_social_links(self):
        # this will return the social links
        return self.profile_social.all()
    
    def get_cart_items(self):
        # get all the users cart itmes
        return self.profile_cart.filter(status="A").all()
    
class SocialPlatformIcon(models.TextChoices):
    IG = "IG", 'fa-instagram'
    FB = "FB", 'fa-facebook-f'
    TW = "TW", 'fa-twitter'
    LD = "LD", 'fa-linkedin'

class SocialLink(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile_social")
    platform = models.CharField(max_length=100,unique=True, help_text="example facebook")
    link = models.URLField(max_length=255)
    icon = models.CharField(max_length=2, choices=SocialPlatformIcon.choices)

@receiver(post_save, sender=MyUser)
def profile_post_save_receiver(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.user_profile.save()
