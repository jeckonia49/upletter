from collections.abc import Mapping
from typing import Any
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from accounts.models import MyUser, Profile, SocialLink, SocialPlatformIcon
from django.forms import BaseModelFormSet, formset_factory

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = MyUser
        fields = ("email",)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ("email", "password", "is_active", "is_admin")

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class LoginModalForm(forms.Form):
    email = forms.EmailField(max_length=100, label="Email Address", widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(max_length=100, label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"}))

    def cleaned_email(self):
        return self.cleaned_data.get("email")    

    def cleaned_password(self):
        return self.cleaned_data.get("password")
    

class RegisterModalForm(UserCreationForm):
    agree_to_terms = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class": "mr-10"}), required=True, label="terms and conditions")

    def cleaned_email(self):
        return self.cleaned_data.get("email")
    
class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ["bio","first_name","last_name"]

    widgets = {
        "first_name":forms.TextInput(attrs={"placeholder": "First Name"}),
        "last_name":forms.TextInput(attrs={"placeholder": "Last Name"}),
        "bio":forms.Textarea(attrs={"placeholder": "More about you", "cols": "30", "rows": '3'}),
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class SocialProfileForm(forms.ModelForm):
    icon = forms.ChoiceField(choices=SocialPlatformIcon.choices,)
    class Meta:
        model = SocialLink
        fields = ["platform","link","icon"]
        widgets = {
            "link":forms.TextInput(),
        }


socialFormSet = formset_factory(SocialProfileForm, extra=1)