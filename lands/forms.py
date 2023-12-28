from typing import Any
from django import forms
from .models import Contact, ItemThreeAbstractModel, Subscription
from posts.models import PostComment


class ItemThreeAbstractModelForm:
    # this is a custom helepr form tha tha willl hold similar field for modek form to avoid duplication of code
    # DRY Principle
    class Meta:
        fields = ['name', 'email', 'message']
        widgets = {
            "name": forms.TextInput(attrs={"id": "name", "placeholder": "Your name"}),
            "email": forms.EmailInput(attrs={"id": "email", "placeholder": "Email Address"}),
            "message": forms.Textarea(attrs={"id": "message", "placeholder": "Sample content"}),
        }

class ContactForm(ItemThreeAbstractModelForm, forms.ModelForm):
    # utilizine the helper form field holder
    class Meta:
        model = Contact
        fields = '__all__'

class SubscriptionForm(forms.ModelForm):
      # utilizine the helper form field holder
    class Meta:
        model = Subscription
        fields = ['email']
        widgets = {
            "email": forms.EmailInput(attrs={"class": "enteremail", "placeholder": "Email address"})
        }