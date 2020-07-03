from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from .models import Post, Image, Category
from .serializers import ImageSerializer, PostSerializer, CategorySerializer
from .paginations import StandardPagination


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = StandardPagination



class PostListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    pagination_class = StandardPagination

    def perform_create(self, serializer):
        # set post's owner
        serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        """Filter posts which are active and have images assigned to them"""
        queryset = Post.objects.filter(is_active=True, images__gt=0).distinct()
        return queryset



class ImageViewSet(viewsets.ModelViewSet):
    """API endpoint for listing, creating, updating and deleting images."""

    serializer_class = ImageSerializer
    pagination_class = StandardPagination

    def perform_create(self, serializer):
        # set image's owner
        serializer.save(owner=self.request.user)
        
    def get_queryset(self):
        """
        Optionally restricts the returned images,
        by filtering against a `post` query parameter in the URL.
        """
        queryset = Image.objects.all()

        post = self.request.query_params.get('post', None)
        category = self.request.query_params.get('category', None)
        
        if post is not None:
            queryset = queryset.filter(post__pk=post)
        
        if category is not None:
            queryset = queryset.filter(category__slug=category)

        return queryset
