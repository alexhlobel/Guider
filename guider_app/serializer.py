from rest_framework import serializers
from .models import Guide, Comment
from django.contrib.auth.models import User


class GuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guide
        fields = ("id", "title", "slug", "text", "image")
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class AdminGuideSerializer(GuideSerializer):
    class Meta:
        model = Guide
        fields = ("id", "moderated", "title", "slug",
                  "text", "image", "created_at")
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True,
                                     style={'input_type': 'password'})
    repeat_password = serializers.CharField(write_only=True,
                                            style={'input_type': 'password'})

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "repeat_password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        username = validated_data["username"]
        password = validated_data["password"]
        repeat_password = validated_data["repeat_password"]
        if password != repeat_password:
            raise serializers.ValidationError(
                {"password": "Пароли не совпадают"})
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user


class UserDetailSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(
        style={'input_type': 'text'}, allow_blank=True)
    last_name = serializers.CharField(
        style={'input_type': 'text'}, allow_blank=True)
    email = serializers.EmailField(
        style={'input_type': 'text'}, allow_blank=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "password", "username", "email")


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True)
    guide = serializers.SlugRelatedField(
        slug_field="slug", read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "guide", "author", "text", "created_date")
        lookup_field = 'id'
        extra_kwargs = {
            'url': {'lookup_field': 'id'}
        }


class GuideLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Guide
        fields = ("id", "title", "slug", "text", "image",
                  "created_at", "total_likes", "total_dislikes")
        read_only_fields = ("id", "title", "slug", "text", "image",
                            "created_at", "total_likes", "total_dislikes")
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GuideDislikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Guide
        fields = ("id", "title", "slug", "text", "image",
                  "created_at", "total_likes", "total_dislikes")
        read_only_fields = ("id", "title", "slug", "text", "image",
                            "created_at", "total_likes", "total_dislikes")
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
