from lands.mixins import get_next_or_prev
from django.http import JsonResponse


class ItemNextPrevMixin:
    """This class make use of the get_next_or_prev func from the lands.mixins."""
    queryset = None
    prev_lookup = "prev"
    next_lookup = "next"

    def get_post_object(self, **kwargs):
        """This method is important not implemented but will be implemented in the following 
        class bellow to get the current object needed by the filter method as used below"""
        pass

    def get_prev_post(self, **kwargs):
        """This method return the previous item if any from the current object"""
        return get_next_or_prev(self.queryset, self.get_post_object(**kwargs), self.prev_lookup)
    
    def get_next_post(self, **kwargs):
        """This method return the next item if any from the current object"""
        return get_next_or_prev(self.queryset, self.get_post_object(**kwargs), self.next_lookup)

    def get_context_data(self, **kwargs):
        """This context dictionary will currry the dictionary to the child class"""
        context = {}
        context["prev_post"] =  self.get_prev_post(**kwargs)
        context["next_post"] =  self.get_next_post(**kwargs)
        return context
    
class CategoryMixin:
    """There is too much repetion of the method (get_all_categories()) for its sensible to create a separate mixin to hundle anad remove repetion"""
    def get_all_categories(self):
        return self.category.objects.all().order_by("-id")[:20]
    
    def get_context_data(self, **kwargs):
        """create a dictionary for data rendering on the template"""
        context = {}
        context['categories'] = self.get_all_categories()
        return context
    

class ItemJsonListViewMixin:
    queryset = None
    
    def get(self, *args, **kwargs):
        upper_limit = kwargs.get("num_items")
        items_size = len(self.queryset.objects.all())
        lower_limit = upper_limit - 3 if items_size > 2 else upper_limit
        items = list(self.queryset.objects.values()[lower_limit:upper_limit])
        max_size = True if upper_limit >= items_size else False
        return JsonResponse({"data": items, "max_size": max_size}, safe=False)
    
