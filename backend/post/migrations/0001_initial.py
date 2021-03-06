# Generated by Django 2.2.13 on 2020-06-28 01:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('slug', models.SlugField(allow_unicode=True, max_length=100, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=250, null=True, verbose_name='title')),
                ('owner_description', models.CharField(blank=True, max_length=4096, null=True, verbose_name='owner description')),
                ('admin_description', models.CharField(blank=True, max_length=4096, null=True, verbose_name='admin description')),
                ('image', models.ImageField(height_field=500, upload_to='images/%Y/%m/%d/', verbose_name='image', width_field=500)),
                ('is_active', models.BooleanField(default=False, verbose_name='is active')),
                ('total_views', models.PositiveIntegerField(default=0, verbose_name='total views')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='create')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='create')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='post.Category', verbose_name='category')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='owner')),
            ],
            options={
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
                'ordering': ['-created'],
            },
        ),
    ]
