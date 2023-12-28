from django.db import models
from accounts.models import Profile
from django.urls import reverse, reverse_lazy
from ._models import CartStatus
from django.db.models import Sum



class Shop(models.Model):
    vendor = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="profile_shop")
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100)
    description = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to="shop/", blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("shops:shop_detail", kwargs={"shop_slug": self.slug})

class Product(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="shop_product")
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100)
    image = models.ImageField(upload_to="product/")
    description=models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=9)
    selling_price = models.DecimalField(decimal_places=2, max_digits=9)
    discount_price = models.DecimalField(decimal_places=2, max_digits=9, default=0.00)
    items_in_stock = models.PositiveIntegerField(default=1)
    reviews = models.IntegerField(default=0)


    def __str__(self):
        return self.name

    
    def get_absolute_url(self):
        """This handle the single object url"""
        return reverse("shops:product_detail", kwargs={"product_slug": self.slug})

    
    def get_add_to_cart_url(self):
        """This handle the single object url"""
        return reverse("shops:product_add_to_cart", kwargs={"product_slug": self.slug})
    
    def get_remove_from_cart_url(self):
        """This handle the single object url"""
        return reverse("shops:product_remove_from_cart", kwargs={"product_slug": self.slug})
    
    def get_product_review_url(self):
        """This handle the single object url"""
        return reverse("shops:product_review", kwargs={"product_slug": self.slug})


    def get_percentage_discount(self):
        """This help in returning the discount price"""
        if float(self.discount_price) > 0.00:
            return f"{float((self.discount_price/self.price) * 100):.2f} %"
        return float(0.00)
    
    def get_selling_price(self):
        """This function will get the selling price in case there is discount price"""
        return float(f"{(self.price - self.discount_price):.2f}")
    
    def get_product_image_slides(self):
        """List all the related images of the products"""
        return self.product_image_slide.all()
    
    def get_product_reviews(self):
        return self.product_review.all().order_by("-timestamp")[:10]
    

    
    def get_product_sum_total(self):
        """This is a kind or unique query; because we have to get the single item 
        based on the name and reveerse it back to the current queryse"""
        # return a float
        # this will allow us get the toal amout

        try:
            # try to get the sum if cart exist else 
            # return the selling price
            return float(f"{(self.product_cart.get(product__name=self.name).item_count * self.get_selling_price()):.2f}")
        except: return self.get_selling_price()


    def save(self, *args, **kwargs):
        """check if there is discount if so then get it and then save a it else th eprice become then selling price"""
        if self.discount_price:
            # if discount then save the selling price
            self.selling_price = self.get_selling_price()
        else:
            # save the sellign price as the price
            self.selling_price = self.price
        return super().save(*args, **kwargs)

class ProductImageSlide(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_image_slide")
    image = models.ImageField(upload_to="product/slides/")

    def __str__(self):
        return f"Product Image Id: {self.pk}"

class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_review")
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    review = models.TextField(max_length=1000)
    ratings = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.full_name

class Cart(models.Model):
    buyer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile_cart")
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name="product_cart")
    item_count = models.IntegerField(default=1)
    status = models.CharField(max_length=3, choices=CartStatus.choices, default=CartStatus.A)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name}: {self.status}"
    
    @property
    def cart_sum_total(self):
        print(self.get_cart_sum_total())
        return self.get_cart_sum_total()
    
    def get_absolute_url(self):
        """because wuill use this for the Order Placement we need this use"""
        return reverse("shops:cart_detail_view", kwargs={"pk": self.pk})
    
    def get_cart_sum_total(self):
        # product_sum = float(f"{(self.count * self.product.get_selling_price()):.2f}")
        # print(product_sum)
        """The method to handle the product summation price is in the context_processor: will take care of it later"""
        return float(f"{(self.__class__.objects.all().aggregate(Sum('product__selling_price'))['product__selling_price__sum'] * self.item_count):.2f}")
    
class OrderItem(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile_order_item")
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_order_item")
    price = models.DecimalField(decimal_places=2, max_digits=9)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.IntegerField()
    city = models.CharField(max_length=100)
    


    def __str__(self):
        return f"{self.full_name}"
    
