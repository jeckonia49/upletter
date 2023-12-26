from django.db import models
from accounts.models import Profile
from django.utils.text import slugify
from tinymce import models as tinymce_models
from django.db.models import Avg, Sum, F, Q, Max
from django.urls import reverse
from lands.models import ItemThreeAbstractModel
from ckeditor.fields import RichTextField


class GenreCategoryAbstract(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    picture = models.ImageField(upload_to="category/", blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        abstract = True
        ordering = ['name']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

class Genre(GenreCategoryAbstract):

    class Meta:
        verbose_name = "genre"
        verbose_name_plural = "genres"

    def get_category_related(self):
        return self.category_genre.all().order_by("-id")[:20]
    
class Category(GenreCategoryAbstract):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="category_genre")
    
    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def get_post_related(self):
        return self.post_category.all().order_by("-id")
    
    def get_absolute_url(self):
        return reverse("posts:category_detail", kwargs={"category_slug": self.slug})
    
class Tag(GenreCategoryAbstract):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    picture = None

class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="post_profile")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="post_category")
    tags = models.ManyToManyField(Tag, blank=True)
    title = models.CharField(max_length=250, unique=True)
    bg_image = models.ImageField(upload_to='posts/')
    cover_image = models.ImageField(upload_to='cover/', blank=True, null=True, help_text="for post detail banner")
    slug = models.SlugField(max_length=250, unique=True)
    summary = models.TextField(blank=True, null=True, max_length=1000)
    content = tinymce_models.HTMLField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=1)
    comments = models.IntegerField(default=0)
    editor_choice = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    
    class Meta:
        ordering=['-timestamp']
        get_latest_by = "timestamp"

    def get_absolute_url(self):
        return reverse("posts:post_detail", kwargs={"post_slug": self.slug})
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    
    def get_image_files_slide(self):
        if self.post_postimageslides.all():
            return self.post_postimageslides.all()
        else: return self.bg_image

    def get_post_comment(self):
        return self.post_comment.all().order_by("-id")
    

class PostImageSlide(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_postimageslides")
    image = models.ImageField(upload_to="post/slides/")

    def __str__(self):
        return f"Post Slide {self.pk}"
    
class PostComment(ItemThreeAbstractModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_comment")

