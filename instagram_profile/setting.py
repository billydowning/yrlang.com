from django.conf import settings

try:
    from .models import InstagramConfiguration
except Exception as e:
    print(e)


class Instagram(object):
    def __init__(self):
        self.instagram_account = 'instagram_account_name'
        self.instagram_auth_url = 'https://api.instagram.com/oauth/authorize'
        self.instagram_access_token_url = 'https://api.instagram.com/oauth/access_token'
        self.instagram_app_id = 1222001741516000
        self.instagram_app_secret = '9cc350de07e062fec41a0f5f80e655ab'
        self.instagram_redirect_url = 'https://127.0.0.1:8000/admin/instagram_profile/post/sync'
        self.instagram_media_url = 'https://graph.instagram.com'

try:
    obj = InstagramConfiguration.objects.filter(active=True).last()

    INSTAGRAM_ACCOUNT = obj.instagram_account or 'instagram_account_name'
    INSTAGRAM_AUTH_URL = obj.instagram_auth_url
    INSTAGRAM_ACCESS_TOKEN_URL = obj.instagram_access_token_url
    INSTAGRAM_APP_ID = obj.instagram_app_id
    INSTAGRAM_SECRET = obj.instagram_app_secret
    INSTAGRAM_REDIRECT_URL = obj.instagram_redirect_url
    INSTAGRAM_MEDIA_URL = obj.instagram_media_url
except Exception as e:
    obj = Instagram()
    print(e)

