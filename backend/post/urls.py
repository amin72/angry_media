from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


app_name = 'post'

router = DefaultRouter()
router.register('images', views.ImageViewSet, basename='image')


urlpatterns = [
    # create or get posts
    path('posts/', views.PostListCreateAPIView.as_view(),
        name='post_list_create'),
    
    # get categories
    path('categories/', views.CategoryListAPIView.as_view(),
        name='category_list'),
]

urlpatterns += router.urls
