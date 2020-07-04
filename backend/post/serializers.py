from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Post, Image, Category


User = get_user_model()



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'title',
            'slug'
        ]



class ImageSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    post = serializers.StringRelatedField()
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Image
        fields = [
            'owner',
            'title',
            'owner_description',
            'admin_description',
            'category',
            'image',
            'post',
            'total_views'
        ]
        
        read_only_fields = [
            'owner',
            'admin_description',
            'post',
            'total_views'
        ]



class PostSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    images = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='post:image_user-detail'
    )

    class Meta:
        model = Post
        fields = [
            'owner',
            'title',
            'description',
            'images',
            'created',
            'updated'
        ]
        
        read_only_fields = [
            'owner',
            'created',
            'updated'
        ]



class PostManageSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.StringRelatedField()
    url = serializers.HyperlinkedIdentityField(
        view_name='post:post_manage-detail')

    class Meta:
        model = Post
        fields = [
            'owner',
            'title',
            'description',
            'is_active',
            'created',
            'updated',
            'url'
        ]
        
        read_only_fields = [
            'owner',
            'created',
            'updated'
        ]



class ImageManageSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.StringRelatedField()
    url = serializers.HyperlinkedIdentityField(
        view_name='post:post_manage-detail')

    class Meta:
        fields = [
            'owner',
            'title',
            'owner_description',
            'admin_description',
            'is_active',
            'category',
            'image',
            'created',
            'updated',
            'post',
            'total_views',
            'url'
        ]
        
        read_only_fields = [
            'owner',
            'total_views',
            'created',
            'updated',
        ]
