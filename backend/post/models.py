from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


User = get_user_model()


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



class Image(models.Model):
    """Image model represent elements of a post"""

    owner = models.ForeignKey("user.CustomUser",
        verbose_name=_("owner"),
        on_delete=models.DO_NOTHING)

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

    image = models.ImageField(_("image"),
        upload_to="images/%Y/%m/%d/",
        height_field=500,
        width_field=500)

    is_active = models.BooleanField(_("is active"), default=False)
    total_views = models.PositiveIntegerField(_("total views"), default=0)
    created = models.DateTimeField(_("create"), auto_now_add=True)
    updated = models.DateTimeField(_("create"), auto_now=True)

    def __str__(self):
        return self.owner.username

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')
        ordering = ['-created']



class Post(models.Model):
    """Post model represent collections of elements"""

    owner = models.ForeignKey("user.CustomUser",
        verbose_name=_("owner"),
        on_delete=models.DO_NOTHING)

    title = models.CharField(_("title"), max_length=250, null=True, blank=True)

    description = models.CharField(_("description"),
        max_length=4096,
        null=True,
        blank=True)

    images = models.ManyToManyField("post.Image", verbose_name=_("images"))

    is_active = models.BooleanField(_("is active"), default=False)
    created = models.DateTimeField(_("create"), auto_now_add=True)
    updated = models.DateTimeField(_("create"), auto_now=True)

    def __str__(self):
        return self.owner.username

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
        ordering = ['-created']
