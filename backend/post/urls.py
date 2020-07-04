from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


app_name = 'post'

router = DefaultRouter()
router.register('images', views.ImageUserViewSet, basename='image_user')
router.register('post_manage', views.PostManageViewSet, basename='post_manage')


urlpatterns = [
    # create or get posts
    path('posts/', views.PostListAPIView.as_view(),
        name='post_list'),
    
    # get categories
    path('categories/', views.CategoryListAPIView.as_view(),
        name='category_list'),
]

urlpatterns += router.urls
