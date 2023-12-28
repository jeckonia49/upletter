from lands.forms import ItemThreeAbstractModelForm
from .models import PostComment
from django import forms


class PostCommentForm(ItemThreeAbstractModelForm, forms.ModelForm):
    """Inherit the Form item holde rform the field Can notice the less code here"""
    class Meta:
        model = PostComment
        exclude = ("post",)
