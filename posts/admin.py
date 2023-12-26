from django.contrib import admin

from .models import (
    Genre, Category, Tag,Post, PostImageSlide, PostComment
)

@admin.register(Genre)
class AdminGenre(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {"slug":("name",)}


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ['genre', 'name']
    prepopulated_fields = {"slug":("name",)}



@admin.register(Tag)
class AdminTag(admin.ModelAdmin):
    list_display = ['name',]
    prepopulated_fields = {"slug": ("name",)}


class PostSlideImageInline(admin.StackedInline):
    model = PostImageSlide
    extra = 0


@admin.register(Post)
class AdminPost(admin.ModelAdmin):
    readonly_fields = ['comments']
    prepopulated_fields = {"slug": ("title",)}
    list_select_related = ['profile', 'category']
    search_fields = ['title']
    list_display = [
        "profile","category","timestamp","updated_at","views",'comments',
    ]
    list_display_links = [
        "profile","category",
    ]
    list_filter = [
        "profile","category",
    ]
    inlines = [PostSlideImageInline, ]


@admin.register(PostComment)
class AdminPostComment(admin.ModelAdmin):
    list_display = ['post', 'name', 'email']
    fieldsets = (
        (None, {"fields": ("post", "name", "email", "message")}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("post", "name", "email", "message"),
            },
        ),
    )
    

