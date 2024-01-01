from posts.models import Post, Category, PostComment, Tag
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    """This will transform the Post model into jSON DataType"""
    class Meta:
        model = Post
        fields = "__all__"

    def create(self, validated_data):

        return super().create(validated_data)
    
    def save(self, **kwargs):
        return super().save(**kwargs)



