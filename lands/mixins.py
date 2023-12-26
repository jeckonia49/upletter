from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage



class HomeGridLandingMixin:
    def get_main_hero_grid1(self,  **kwargs):
        return self.queryset.objects.all().order_by("?").first()

    def get_main_hero_grid2(self,  **kwargs):
        return self.queryset.objects.all().order_by("?").first()

    def get_main_hero_grid3(self,  **kwargs):
        return self.queryset.objects.all().order_by("?").first()

    def get_main_hero_grid4(self,  **kwargs):
        return self.queryset.objects.all().order_by("?").first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_g1'] = self.get_main_hero_grid1(**kwargs)
        context['main_g2'] = self.get_main_hero_grid2(**kwargs)
        context['main_g3'] = self.get_main_hero_grid3(**kwargs)
        context['main_g4'] = self.get_main_hero_grid4(**kwargs)
        return context
    
class HomeTopLandinMixin:
    def get_home_top_posts(self, **kwargs):
        return self.queryset.objects.all().order_by("?")[:2]
    
    def get_home_top_swiper_posts(self, **kwargs):
        return self.queryset.objects.filter(editor_choice=True).all().order_by("?")[:5]
    
    def get_home_lower_posts(self, **kwargs):
        return self.queryset.objects.all()[:5]
    
    def get_trending_posts(self, **kwargs):
        return self.queryset.objects.all().order_by("-timestamp")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_posts'] = self.get_home_top_posts(**kwargs)
        context['top_swiper'] = self.get_home_top_swiper_posts(**kwargs)
        context['lower_posts'] = self.get_home_lower_posts(**kwargs)
        context['trending'] = self.get_trending_posts(**kwargs)
        return context
    
class PaginationMixin:
    queryset = None
    page_kwargs = "page"
    paginate_by = 4
    context_object_name = ""

    def get_queryset_from_latest(self, **kwargs):
        return self.queryset.objects.all().order_by("-timestamp")

    def get_context_data(self, **kwargs):
        page_number = self.request.GET.get(self.page_kwargs)
        paginator = Paginator(self.get_queryset_from_latest(**kwargs), self.paginate_by)
        page_range = paginator.get_elided_page_range(number=page_number)
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
             # If the page number is not an integer, set page to the first page
            page = paginator.page(1)
        except EmptyPage:
            # If the page number is out of range (e.g., greater than the number of pages), set page to the last page
            page = paginator.page(paginator.num_pages)
        
        if page.has_next():
            next_url = "?{kw}={n}".format(kw=self.page_kwargs, n=page.next_page_number())
        else: next_url = None

        if page.has_previous():
            prev_url = "?{kw}={n}".format(kw=self.page_kwargs, n=page.previous_page_number())
        else: prev_url = None

        context = {}

        context[self.context_object_name] = page
        context['next_url'] = next_url
        context['prev_url'] = prev_url
        context['page_range'] = page_range
        context['is_paginated'] = page.has_other_pages()
        return context
    
def get_next_or_prev(queryset, item, direction):
    """
    This function is to help in the getting the ext and the previous itme from the current itme
    Direction == prev (for previous item if any)
    Direction == next (for next item if any)
    """
    getit=False
    if direction == "prev":
        queryset = queryset.reverse()
    elif direction == "next":
        queryset = queryset
    for obj in queryset:
        if getit:
            return obj
        if item == obj:
            getit = True
    if getit:
        # this will happend when the last item 
        # made getiit true
        return queryset[0]
    return False


    


