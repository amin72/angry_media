from django.contrib import admin
from .models import Post, Category, Comment, Image


admin.site.register(Post)
admin.site.register(Image)
admin.site.register(Category)
admin.site.register(Comment)
