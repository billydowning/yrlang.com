from _ast import mod
from django.shortcuts import reverse
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
import os
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

# wagtail
from wagtail.snippets.models import register_snippet
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Page

from .managers import CustomUserManager
from django.contrib.gis.db import models as gis_model


@register_snippet
class State(models.Model):
    name = models.CharField(max_length=50)
    location = gis_model.PointField(null=True, blank=True)

    panels = [
        FieldPanel('name')
    ]

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


@register_snippet
class Language(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, null=True,
                                   blank=True,
                                   help_text='Describe about language.'
                                   )
    panels = [
        FieldPanel('name'),
        FieldPanel('description')
    ]

    def __str__(self):
        return self.name


class Profession(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class UserRole(models.Model):
    CLIENT = 'client'
    LOCALITE = 'localite'
    PROVIDER = 'provider'
    LANGUAGE_VERIFIER = 'language_verifier'
    ROLE_CHOICES = (
        (CLIENT, 'Client'),
        (LOCALITE, 'Localite'),
        (PROVIDER, 'Provider'),
        (LANGUAGE_VERIFIER, 'Language Verifier')

    )
    name = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    bio = models.TextField(null=True, blank=True)
    phone_number = models.CharField(null=True, blank=True, max_length=15)
    state = models.ForeignKey(State, null=True, blank=True, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.CASCADE)
    is_client = models.BooleanField(default=True)
    language = models.ManyToManyField(Language, null=True, blank=True)
    profession = models.ManyToManyField(Profession, null=True, blank=True)
    stripe_id = models.CharField(max_length=200, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    user_role = models.ManyToManyField(UserRole, null=True, blank=True)
    is_private = models.BooleanField('private', default=False)
    multi_day = models.BooleanField(default=False)
    last_location = gis_model.PointField(null=True, blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    @classmethod
    def get(cls, id):
        return cls.objects.get(id=id)

    def is_client_user(self, role):
        return UserRole.CLIENT == role

    def is_provider_user(self, role):
        return UserRole.PROVIDER == role

    def is_localite_user(self, role):
        return UserRole.LOCALITE == role

    def is_language_verifier_user(self, role):
        return UserRole.LANGUAGE_VERIFIER == role

    def get_provider_absolute_url(self):
        return reverse('provider_detail', args=[self.pk])

    def get_public_profile(self):
        return reverse('public_profile', args=[self.pk])


class UserLanguage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)


class Categories(Page):
    name = models.CharField(max_length=100)

    content_panels = Page.content_panels + [
        FieldPanel('name'),

    ]

    parent_page_types = ['CategoriesIndex']

    def __str__(self):
        return self.name


class ProviderCategories(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    provider = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('category', 'provider')

    def __str__(self):
        return '{} - {}'.format(self.category, self.provider.username)


class CategoriesIndex(Page):
    name = models.CharField(max_length=30, null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('name'),

    ]
    subpage_types = ['Categories']


class UserRoleRequest(models.Model):
    REQUESTED = 'requested'
    APPROVED = 'approved'
    CANCELED = 'canceled'
    VERIFIED = 'verified'

    STATUS_CHOICES = [
        (REQUESTED, 'Requested By Client'),
        (APPROVED, 'Approved By Admin'),
        (CANCELED, 'Canceled By Admin'),
        (VERIFIED, 'Verified By Admin')
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='request_user')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=REQUESTED)
    requested_for = models.ForeignKey(UserRole, on_delete=models.CASCADE, related_name='request_for')
    reason = models.TextField(null=True, blank=True)
    meeting_on =  models.DateTimeField(null=True, blank=True)
    approved_on = models.DateTimeField(null=True, blank=True)
    requested_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} requested for {}'.format(self.user.username, self.requested_for.name)

    def get_detail(self):
        return reverse('client_request_detail', args=[self.pk])


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.mp4', '.m4a', '.m4v', '.avi']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


class UserVideos(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    language = models.ForeignKey(Language, null=True, blank=True, on_delete=models.CASCADE)
    files = models.FileField(validators=[validate_file_extension]
        , upload_to='videos/', null=True, blank=True)

    def __str__(self):
        return '{} Video,for {}'.format(self.content_object.user.username, self.language)

class UserFavorite(models.Model):
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE, related_name='user_favorite')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()




