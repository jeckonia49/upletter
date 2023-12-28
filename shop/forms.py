from django import forms
from .models import Cart, ProductReview, OrderItem
from lands.forms import ItemThreeAbstractModelForm


class AddToCartForm(forms.ModelForm):
    class Meta:
        exclude = "__all__"
        model = Cart

class ProductReviewForm(forms.ModelForm):
    class Meta:
        fields = ['full_name', 'email', 'review']
        model = ProductReview
        widgets = {
            "full_name":forms.TextInput(attrs={"placeholder": "Your Name"}),
            "email":forms.EmailInput(attrs={"placeholder": "Your Name"}),
            "review":forms.Textarea(attrs={"placeholder": "Your Review"}),
        }

class CheckoutForm(forms.ModelForm):
    class Meta:
        fields = ['full_name', 'email', 'phone', 'city']
        model = OrderItem
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Full Name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email Address"}),
            "phone": forms.TextInput(attrs={"placeholder": "Phone Number"}),
            "city": forms.TextInput(attrs={"placeholder": "City/Location"}),
        }