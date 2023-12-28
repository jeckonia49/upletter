from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from lands.mixins import PaginationMixin, ObjectMixin, SearchQueryView
from posts.mixins import CategoryMixin
from .models import Shop, Product
from posts.models import Category
from django.http.response import HttpResponse as HttpResponse
from .models import Product, Cart, OrderItem
from django.contrib import messages
from django.views.generic import View
from accounts.views import SuccessUrlRedirect
from django.db.models import Sum, Avg,  Q
from django.contrib.auth import get_user
from .forms import ProductReviewForm, CheckoutForm
from .context_processor import get_cart_total_summation

class CustomLoginRequiredMixinView(SuccessUrlRedirect, View):
    """Ive also passed the SuccessUrlRedirect from accounts.views to be used for the current page redirect"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You'll need to the logged in first!")
            """Implemented here"""
            return self.get_success_url(*args, **kwargs)
        """If user session is active the  proceed"""
        return super().dispatch(request, *args, **kwargs)
    
    def get_user_profile(self):
        """Get the user profile"""
        return get_user(self.request).user_profile

class RemoveProductFromCartView(ObjectMixin, CustomLoginRequiredMixinView):

    """This mixin Object defined in lands.mixins will get use the exact product on the cart
    You can notice how this is helping in avoiding code duplication !!!
    """
    queryset = Product
    lookup_slug_field = "product_slug"

    def post(self, request, *args, **kwargs):
        """This will be our onli login now| what will work on more"""
        product = self.get_item_object(**kwargs)
        # now get the cart with the poduct and delete it based on the clearance
        cart = Cart.objects.filter(product=product).all()
        # if remove from cart then check the name of the product and identify how many 
        # based on the pk so that we can update theire count on the  
        # items in stoke field
        for item in cart:
            # check if the product in the cart have the id off the product 
            # if so then update the count

            if item.product.id == product.id:
                # find the total summation of the product pk of the current item and the add it 
                # on the pk of the available and the add
                # we need to filter so that we only get the field we need
                item_count__sum = cart.filter(product__pk=item.product.pk).aggregate(Sum("item_count"))['item_count__sum']
                # after this we can then add then
                item.product.items_in_stock += item_count__sum
                # save the product and then just proceed to 
                # delete the prodcut
                item.product.save()
        # now we can delete the cart
        messages.info(request, "Cart Produt deleted")
        cart.delete()
        """I can use theis method because it's in the CustomLoginRequiredMixinView which is parent of this current class"""
        return self.get_success_url(**kwargs)

class AddProductToCartView(ObjectMixin, CustomLoginRequiredMixinView):
    """This will be almost like removal but with litlte more modfication"""
    queryset = Product
    lookup_slug_field = "product_slug"
    cart_item = Cart

    # 
    def post(self, request, *args, **kwargs):
        product = self.get_item_object(**kwargs)
        profile = request.user.user_profile
        """# now look if there is product in the cart"""
        """
            Try get the item from the url and then check if that item is inside the cart
            if yes update the count fild else add it to the cart
            """
        cart_item = self.cart_item.objects.filter(product=product, buyer=profile)
        if cart_item.exists():
            """# now that cart already have the product will juts update the count on the cart"""
            # reduce the product by 1 for each addition to the cart
            if product.items_in_stock > 0:
                product.items_in_stock -= 1
                product.save()
                cart = cart_item.first()
                cart.item_count += 1
                cart.save()
            """After this will return the request with the success message"""
            messages.success(request, "Product Quantity Updated on the cart!")
            return self.get_success_url(**kwargs)
        
        elif not cart_item.exists():
            """Now that there is not product on the cart we create the cart"""
                # reduce the product by 1 for each addition to the cart
            if product.items_in_stock > 0:
                product.items_in_stock -= 1
                product.save()
                cart_item = Cart.objects.create(buyer=profile, product=product).save()
            """Save the cart and the update th euser and then redietc to the same view"""
            messages.success(request, "Product added to cart successfully")
            return self.get_success_url(**kwargs)
        """Incase of any error|netwoek|unkwonwn|etc"""
        messages.error(request, "There was an error processing the request. Kindly retry!")
        return self.get_success_url(**kwargs)

class ShopView(PaginationMixin, SearchQueryView, CategoryMixin, TemplateView):
    template_name = "shop/shop_view.html"
    queryset = Product
    category = Category
    paginate_by = 100
    context_object_name = "posts"
    cart=Cart
    search_query = "product_query"
    

    def get_queryset_from_latest(self, **kwargs):
        """Override the method toallow specific filtration"""
        if self.get_search_query_term() is not None:
            """Filter the posts but take into acount the current category we are at
            The posts fil will be filtered but the category will have to remain the current cateory so only
            """

            return self.queryset.objects.filter(
                shop__is_verified=True, items_in_stock__gte=1).filter(
                Q(name__icontains=self.get_search_query_term())
            ).all()
        # if not item the proceed with the posts
        return self.queryset.objects.all().filter(shop__is_verified=True, items_in_stock__gte=1).order_by("?")
    
    def get_profile(self):
        """Self  explanatory"""
        return get_user(self.request).user_profile
    
    
    def get_context_data(self, **kwargs):
        context = super(ShopView, self).get_context_data(**kwargs)
        context[self.context_object_name] = self.get_queryset_from_latest(**kwargs)
        context['categories'] = self.get_all_categories()
        return context
    
class ShopProductDetailView(ObjectMixin, CategoryMixin, TemplateView):
    """
    This objectmixin from lands.mixins will return the single object based on the lookup filed provided
    This kind of inheritance help alot in removing code duplication
    """
    queryset = Product
    lookup_slug_field = "product_slug"
    template_name = "shop/(product)/product_detail.html"
    cart=Cart
    category=Category
    form_class = ProductReviewForm


    def get_product_item(self, **kwargs):
        """We also need to filter """
        try: return self.cart.objects.filter(buyer=self.request.user.user_profile, product=self.get_item_object(**kwargs), status="A").first()
        except: return None
    
    def get_product_reviews(self):
        pass

    def get_related_products(self, **kwargs):
        """This will return the  products from the same shop"""
        instance = self.get_item_object(**kwargs)
        return self.queryset.objects.filter(
            shop__name=instance.shop.name
            ).all().exclude(name=instance.name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.get_item_object(**kwargs)
        context['similar_products']=self.get_related_products(**kwargs)
        context['cart'] = self.get_product_item(**kwargs)
        context['form'] = self.form_class()
        return context

class ProductReviewView(ObjectMixin,SuccessUrlRedirect, View):
    """Inherit the single object mixin to handle the single object retrival"""
    form_class = ProductReviewForm
    queryset = Product
    lookup_slug_field = "product_slug"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.product=self.get_item_object(**kwargs)
            instance.product.reviews+=1
            instance.product.save()
            form.save()
            return self.get_success_url(*args, **kwargs)
        return self.get_success_url(*args, **kwargs)

class CustomCartListViewMixin(CustomLoginRequiredMixinView, TemplateView):
    """This class will handle the cart and the checkpout coz the logic is more similar so we avoid code duplication"""
    queryset = Cart

    def get_cart_products(self):
        """This return the cart item which hold the entire product"""
        return self.queryset.objects.filter(buyer=self.get_user_profile(), status="A").all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_products'] = self.get_cart_products()
        return context

class CartListView(CustomCartListViewMixin):
    """This will be the only implementation"""
    template_name = "shop/cart/cart_list.html"

class CartCheckoutView(CustomCartListViewMixin):
    """Same as abouve but will implement the checkout form"""
    form_class = CheckoutForm
    model = OrderItem
    template_name = "shop/cart/checkout.html"


    def get_cart_checkout_total(self,**kwargs):
        """Am using most of the codes from remove from card explanation is in there for reference
        However this is going to be a little deeper in terms of looping to make it work"""

        # now get the cart with the poduct and delete it based on the clearance
        cart_items = self.get_cart_products()
        products = None
        for item in cart_items:
            products = cart_items.select_related("product").filter(product__pk=item.product.pk).aggregate(Sum("product__price"))
        # if remove from cart then check the name of the product and identify how many 
        # based on the pk so that we can update theire count on the  
        # items in stoke field
        # for item in cart_items:
        #     # check if the product in the cart have the id off the product 
        #     # if so then update the count

        #     if item.product.id == product.id:
        #         # find the total summation of the product pk of the current item and the add it 
        #         # on the pk of the available and the add
        #         # we need to filter so that we only get the field we need
        #         item_count__sum = cart.filter(product__pk=item.product.pk).aggregate(Sum("item_count"))['item_count__sum']
        #         # after this we can then add then
        #         item.product.items_in_stock += item_count__sum
        #         # save the product and then just proceed to 
        #         # delete the prodcut
        #         item.product.save()
        # # now we can delete the cart
        # cart.delete()
        # """I can use theis method because it's in the CustomLoginRequiredMixinView which is parent of this current class"""
        # return
        return products


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        return context
    
    def get_profile_cart_items(self):
        """This will ensure that their is a cart item"""
        cart = self.get_cart_products().filter(status="A").first()
        return cart
    
    
    def dispatch(self, request, *args, **kwargs):
        """Override this to ensure that the user and the cart has an object else redirect to the shop face"""
        if not request.user.is_authenticated:
            """This will ensure that the user is authenticate"""
            messages.error(request, "You'll need to the logged in first!")
            """Implemented here"""
            return self.get_success_url(*args, **kwargs)
        """If user session is active the  proceed"""
        if not self.get_profile_cart_items() and request.user.is_authenticated:
            """This will ensure that if there is cart then will be able to proceed eslse be redirected to the shop viw"""
            messages.warning(request, "Your cart is currently empty!")
            """Then redirect to the shopping page"""
            return redirect("shops:shop_view")
        return super().dispatch(request, *args, **kwargs)
    
    
    def post(self, request, *args, **kwargs):
        """Get the users """
        # profile
        profile = self.get_user_profile()
        
        form = self.form_class(request.POST)
        if form.is_valid():
            # hold saving the cart
            instance = form.save(commit=False)
            # save the profile
            instance.profile = profile
            # save the cart
            instance.cart = self.get_profile_cart_items()
            # save the price to be paid
            instance.price = get_cart_total_summation(request)
            # instance.price.save()
            # remove the items from the cart
            instance.cart.status="D"
            instance.cart.save()
            # instance.save()
            form.save()
        return self.get_success_url(*args, **kwargs)






