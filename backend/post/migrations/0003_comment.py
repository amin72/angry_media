# Generated by Django 2.2.13 on 2020-06-28 02:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0002_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_pk', models.TextField(verbose_name='object ID')),
                ('content', models.CharField(max_length=3000, verbose_name='content')),
                ('is_removed', models.BooleanField(default=False, help_text='Check this box if the comment is inappropriate. A "This comment has been removed" message will be displayed instead.', verbose_name='is removed')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, unpack_ipv4=True, verbose_name='IP address')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='create')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='create')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content_type_set_for_comment', to='contenttypes.ContentType', verbose_name='content type')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comment_comments', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'comment',
                'verbose_name_plural': 'comments',
                'ordering': ['created'],
            },
        ),
    ]
