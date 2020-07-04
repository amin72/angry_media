from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from .models import Post, Image, Category
from .serializers import (
    ImageSerializer,
    PostSerializer,
    CategorySerializer,
    PostManageSerializer
)
from .paginations import StandardPagination
from .permissions import IsAuthorOrReadyOnly, IsOwnerAllowedToEditImage


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = StandardPagination



class PostListAPIView(generics.ListAPIView):
    """API endpoint for listing posts."""

    serializer_class = PostSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        """Filter posts which are active and have images assigned to them"""
        queryset = Post.objects.filter(is_active=True, images__gt=0).distinct()
        return queryset



class ImageUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listing, creating, updating and deleting images.
    Queryset is filtered for specific user.
    """

    serializer_class = ImageSerializer
    permission_classes = [
        IsAuthenticated,
        IsAuthorOrReadyOnly,
        IsOwnerAllowedToEditImage
    ]
    pagination_class = StandardPagination

    def perform_create(self, serializer):
        # set image's owner
        serializer.save(owner=self.request.user)
        
    def get_queryset(self):
        """Filter owner's images."""
        queryset = Image.objects.filter(owner=self.request.user)
        return queryset



class PostManageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listing, creating, updating and deleting posts by admin.
    """

    queryset = Post.objects.all()
    serializer_class = PostManageSerializer
    pagination_class = StandardPagination

    def perform_create(self, serializer):
        # set post's owner
        serializer.save(owner=self.request.user)
