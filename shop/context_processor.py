from django.db.models import Q, Sum
from shop.models import Product, Cart

# """This function need to be global : will be back on it """
def get_cart_total_summation(request):
    try:
        """This function however has issues: TODO WILL BE BACK ON IT"""
        # find all the prodcu based on the pricing
        pricing = Cart.objects.filter(
            buyer=request.user.user_profile, status="A", 
            product__selling_price__isnull=False
            ).all().aggregate(Sum("product__selling_price"))
        # Try fix this
        # cart_items = Cart.objects.filter(buyer=request.user.user_profile, status="A").all()
        # if cart_items.exists():
        #     for item in cart_items():
        #         if item.product.pk==
            # find all the prodcu based on the item count
        print(pricing)
        item_list = Cart.objects.filter(
            buyer=request.user.user_profile, 
            status="A").all().select_related("product__pk").aggregate(Sum("item_count"))
        
        return float(f"{(pricing['product__selling_price__sum'] * item_list['item_count__sum']):.2f}")
    except: return None
    
def shop_context_processor_data(request):
    return dict(
        popular_product=Product.objects.filter(reviews__gte=200).all()[:5],
        cart_sum_total=get_cart_total_summation(request),
    )

