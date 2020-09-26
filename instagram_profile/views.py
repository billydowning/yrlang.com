from django.shortcuts import render
from django.conf import settings
from .models import Post


def feed(request):
    data = Post.objects.all()[:50]
    return render(request, 'instagram_profile/feed.html', {
        'feed': data,
        'MEDIA_URL': settings.MEDIA_URL
    })