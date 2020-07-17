from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings


COMMENT_MAX_LENGTH = getattr(settings, 'COMMENT_MAX_LENGTH', 3000)


class Category(models.Model):
    """Category model represent elements category"""

    title = models.CharField(_("title"), max_length=100)
    slug = models.SlugField(_("slug"), max_length=100, allow_unicode=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['title']



class Post(models.Model):
    """Post model represent collections of elements"""

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
        verbose_name=_("owner"),
        on_delete=models.DO_NOTHING)

    title = models.CharField(_("title"), max_length=250, null=True, blank=True)

    description = models.CharField(_("description"),
        max_length=4096,
        null=True,
        blank=True)
    
    is_active = models.BooleanField(_("is active"), default=False)
    created = models.DateTimeField(_("create"), auto_now_add=True)
    updated = models.DateTimeField(_("create"), auto_now=True)

    def __str__(self):
        return f'{self.id} - {self.owner.username}'

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
        ordering = ['-created']



class Image(models.Model):
    """Image model represent elements of a post"""

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
        verbose_name=_("owner"),
        on_delete=models.DO_NOTHING)

    post = models.ForeignKey("post.Post",
        related_name='images',
        verbose_name=_("post"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    title = models.CharField(_("title"), max_length=250, null=True, blank=True)

    owner_description = models.CharField(_("owner description"),
        max_length=4096,
        null=True,
        blank=True)
    
    admin_description = models.CharField(_("admin description"),
        max_length=4096,
        null=True,
        blank=True)

    category = models.ForeignKey("post.Category",
        verbose_name=_("category"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    image_height = models.PositiveIntegerField(_("Image Height"), default=500)
    image_width = models.PositiveIntegerField(_("Image Width"), default=500)

    image = models.ImageField(_("image"),
        upload_to="images/%Y/%m/%d/",
        height_field='image_height',
        width_field='image_width')
    
    total_views = models.PositiveIntegerField(_("total views"), default=0)
    created = models.DateTimeField(_("create"), auto_now_add=True)
    updated = models.DateTimeField(_("create"), auto_now=True)

    def __str__(self):
        return f'{self.id} - {self.owner.username}'

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')
        ordering = ['-created']



class Comment(models.Model):
    """Comment model represents users' comments on the website"""

    content_type = models.ForeignKey(ContentType,
        verbose_name=_('content type'),
        related_name="content_type_set_for_%(class)s",
        on_delete=models.CASCADE)

    object_pk = models.TextField(_('object ID'))
    content_object = GenericForeignKey("content_type", "object_pk")

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        verbose_name=_('user'),
        blank=True,
        null=True,
        related_name="%(class)s_comments",
        on_delete=models.SET_NULL)

    content = models.CharField(_('content'), max_length=COMMENT_MAX_LENGTH)

    is_removed = models.BooleanField(_('is removed'), default=False,
        help_text=_('Check this box if the comment is inappropriate. '
                    'A "This comment has been removed" message will '
                    'be displayed instead.'))


    ip_address = models.GenericIPAddressField(_('IP address'),
        unpack_ipv4=True,
        blank=True,
        null=True)

    created = models.DateTimeField(_("create"), auto_now_add=True)
    updated = models.DateTimeField(_("create"), auto_now=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}..."

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
        ordering = ['created']
