from django.db import models


class Post(models.Model):

    class Meta:
        db_table = 'instagram_posts'
        ordering = ['-created']

    TYPE_IMAGE = 'IMAGE'
    TYPE_VIDEO = 'VIDEO'
    TYPE_ALBUM = 'CAROUSEL_ALBUM'
    MEDIA_TYPES = [
        (TYPE_IMAGE, 'Image'),
        (TYPE_ALBUM, 'Album'),
        (TYPE_VIDEO, 'Video')
    ]

    media_id = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=MEDIA_TYPES, default=TYPE_IMAGE)
    permalink = models.CharField(max_length=256)
    caption = models.TextField(default='')
    thumbnail = models.CharField(max_length=256, default='')
    children = models.TextField(default='')
    created = models.DateTimeField()

    def children_list(self):
        return self.children.split('\n')

    def __str__(self):
        return self.media_id + ' ' + self.type + ' ' + self.caption


class InstagramConfiguration(models.Model):
    instagram_account = models.CharField(max_length=256)
    instagram_auth_url = models.CharField(max_length=256)
    instagram_access_token_url = models.CharField(max_length=256)
    instagram_app_id = models.CharField(max_length=256)
    instagram_app_secret = models.CharField(max_length=256)
    instagram_redirect_url = models.CharField(max_length=256)
    instagram_media_url = models.CharField(max_length=256)
    active = models.BooleanField(default=False)

    def __str__(self):
        return '{} - {} - {}'.format(self.pk, self.instagram_account, self.active)
