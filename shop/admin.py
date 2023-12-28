from django.contrib import admin
from.models import Shop, Product, ProductReview, ProductImageSlide, Cart, ProductReview, OrderItem


class ProductImageSlideInline(admin.StackedInline):
    model = ProductImageSlide
    extra = 0

class ProductReviewInline(admin.StackedInline):
    model = ProductReview
    extra = 0

@admin.register(Shop)
class AdminShop(admin.ModelAdmin):
    list_display = ['vendor', 'name', 'is_verified']
    actions = ("verify_shop", "invalidate_shop")
    prepopulated_fields = {"slug": ("name", )}

    @admin.action(description="Verify Shop")
    def verify_shop(self, request, queryset):
        queryset.update(is_verified=True) 

    @admin.action(description="Invalidate Shop")
    def invalidate_shop(self, request, queryset):
        queryset.update(is_verified=False)

@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ['shop', 'name', 'price', 'discount_price', 'items_in_stock', 'selling_price']
    prepopulated_fields = {"slug": ("name", )}
    readonly_fields = ("selling_price", )
    inlines = [
        ProductImageSlideInline,
        ProductReviewInline
    ]

@admin.register(Cart)
class AdminCart(admin.ModelAdmin):
    list_display = ['buyer', 'product', 'item_count', 'timestamp', 'status', 'cart_sum_total']
    list_filter = ['buyer', 'status']
    
@admin.register(ProductReview)
class AdminProductReview(admin.ModelAdmin):
    list_display = ['product','full_name', 'email','timestamp']

@admin.register(OrderItem)
class AdminOrderItem(admin.ModelAdmin):
    list_display = ['profile','cart', 'price','full_name', 'email', 'phone', 'city']

