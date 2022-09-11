from rest_framework import serializers
from .models import Guide, Comment
from django.contrib.auth.models import User


class PostSerializer(serializers.ModelSerializer):

    creator = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())

    class Meta:
        model = Guide
        fields = ("id", "title", "slug", "text", "image", "created_at", "creator")
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    guide = serializers.SlugRelatedField(slug_field="slug", queryset=Guide.objects.all())

    class Meta:
        model = Comment
        fields = ("id", "guide", "author", "text", "created_date")
        lookup_field = 'id'
        extra_kwargs = {
            'url': {'lookup_field': 'id'}
        }
