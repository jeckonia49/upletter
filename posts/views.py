from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, View
from lands.mixins import PaginationMixin, ObjectMixin, SearchQueryView
from .models import Genre, Post, Tag, Category
from .mixins import CategoryMixin, ItemNextPrevMixin, ItemJsonListViewMixin
from django.db.models import Q
from .forms import PostCommentForm
from accounts.views import SuccessUrlRedirect
from django.contrib import messages


    
# Create your views here.
class PostListView(PaginationMixin,SearchQueryView,CategoryMixin, TemplateView):
    """
    This inherits from pagination to handle pagination,
    CategoryMixin removes duplication from the code
    TemplateView is a helper class for handling the view logic
    """
    template_name = "posts/index.html"
    queryset = Post
    genre = Genre
    category = Category
    paginate_by = 30
    context_object_name = "posts"
    search_query = "search_queryset"


    def get_queryset_from_latest(self, **kwargs):
        if self.get_search_query_term() is not None:
            # check if the is search query and the filter the queryset by filtering the posts based on the title else return the 
            return self.queryset.objects.filter(
                Q(title__icontains=self.get_search_query_term())|
                Q(category__name__icontains=self.get_search_query_term())
                ).all().order_by("-timestamp")
        # proceed to return the parrent method
        return super().get_queryset_from_latest(**kwargs)

    def get_all_genre(self):
        """
        Get hold of all the genras and list the last 10 items in asc order"""
        return self.genre.objects.all().order_by("-id")[:10]
    
    def get_context_data(self, **kwargs):
        """
        Create adictionary of the data from the datable for posting on the templates
        The super method help to grab even the data prepared on the inheritend classes so we 
        dont have to re-declare them here
        """
        context = super().get_context_data(**kwargs)
        context['genres'] = self.get_all_genre()
        print(self.get_search_query_term())
        return context
    
class PostDetailView(ItemNextPrevMixin, CategoryMixin,ObjectMixin, TemplateView):
    template_name = "posts/post.html"
    queryset = Post
    category=Category
    comment_form_class = PostCommentForm
    lookup_slug_field = "post_slug"

    def get_post_object(self, **kwargs):
        # this method is needed to handle the next and the previous url
        return self.get_item_object(**kwargs)

    def get_related_posts(self, **kwargs):
        """In this method we look for related posts based on the category but exclue the current post 
        form the listing
        """
        instance = self.get_item_object(**kwargs)
        return self.queryset.objects.filter(
            Q(category__name=instance.category.name) and ~Q(title=instance.title)
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.get_item_object(**kwargs)
        context['related'] = self.get_related_posts(**kwargs)
        context["comment_form"] = self.comment_form_class()
        return context
    
    def get(self, request: HttpRequest, *args, **kwargs):
        post = self.get_item_object(**kwargs)
        post.views += 1
        post.save()
        return super().get(request, *args, **kwargs)

class PostDetailCommentCreateView(SuccessUrlRedirect, View):
    form_class = PostCommentForm
    queryset = Post

    def get_post_object(self, **kwargs):
        """This method gets the current item(post)"""
        return get_object_or_404(self.queryset, slug=kwargs.get("post_slug"))
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.post = self.get_post_object(**kwargs)
            instance.post.comments += 1
            instance.post.save()
            form.save()
            messages.success(request, "Comment saved successfully")
            print(form.cleaned_data)
            return self.get_success_url(**kwargs)
        messages.error(request, "Error commenting. Retry!")
        return self.get_success_url(**kwargs)
        
class CategoryPostListView(PaginationMixin,SearchQueryView, CategoryMixin, TemplateView):
    """
    This inherits from pagination to handle pagination,
    CategoryMixin removes duplication from the code
    TemplateView is a helper class for handling the view logic
    """
    template_name = "posts/category/index.html"
    context_object_name = "posts"
    queryset = Post
    paginate_by = 30
    model = Category
    search_query = "search_queryset"

    def get_page_slug_url_field(self, **kwargs):
        """This method filter the category object from the database by checking the slug picked from the url with that of the for category object in the category column"""
        return get_object_or_404(self.model, slug=kwargs.get("category_slug"))

    def get_queryset_from_latest(self, **kwargs):
        """
        This method on the paginationmixin is overidded to link it with the category appropriately
        """
        if self.get_search_query_term() is not None:
            """Filter the posts but take into acount the current category we are at
            The posts fil will be filtered but the category will have to remain the current cateory so only
            """
            return self.queryset.objects.filter(
                Q(title__icontains=self.get_search_query_term())
            ).filter(category=self.get_page_slug_url_field(**kwargs)).all()
        # if not item the proceed with the posts
        return self.queryset.objects.filter(category=self.get_page_slug_url_field(**kwargs))
    
    def get_context_data(self, **kwargs):
        """
        Compose a dictionary to render on the template
        """
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_page_slug_url_field(**kwargs)
        print(context)
        return context
        
class PostListSearchView(PaginationMixin, TemplateView):
    queryset = Post
    context_object_name = "posts"
    template_name = "search.html"

    def get_search_queryset(self):
        query = self.request.GET.get("post_qs")
        return query

    def get_queryset_from_latest(self, **kwargs):
        items = self.queryset.objects.filter(title__icontains=self.get_search_queryset()).all().order_by("-timestamp")
        return items
