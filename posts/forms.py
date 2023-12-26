from lands.forms import ItemThreeAbstractModelForm
from .models import PostComment
from django import forms


class PostCommentForm(ItemThreeAbstractModelForm, forms.ModelForm):
    class Meta:
        model = PostComment
        exclude = ("post",)
