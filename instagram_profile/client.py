import json
import requests
from urllib.parse import urlencode
from datetime import datetime
from . import setting


def get_media_feed(auth_code):
    access_token = get_access_token(auth_code)
    if not access_token:
        raise Exception('Invalid authentication code')

    posts = []
    url = setting.INSTAGRAM_MEDIA_URL + '/me/media'
    query = {
        'fields': 'caption,id,media_type,media_url,permalink,thumbnail_url,timestamp,children',
        'access_token': access_token
    }
    res = requests.get(url, params=query)
    if res.status_code == 200:
        feed = json.loads(res.text)
        for item in feed['data']:
            post = convert_media(item)
            if 'children' in item:
                post['children'] = []
                for child in item['children']['data']:
                    data = get_media_details(child['id'], access_token)
                    if data:
                        post['children'].append(data)
            posts.append(post)

    return posts


def get_media_details(id, access_token):
    post = None
    url = setting.INSTAGRAM_MEDIA_URL + '/' + id
    query = {
        'fields': 'id,media_type,media_url,permalink,thumbnail_url,timestamp',
        'access_token': access_token
    }
    res = requests.get(url, params=query)
    if res.status_code == 200:
        post = convert_media(json.loads(res.text))
    return post


def get_auth_url():
    url = setting.INSTAGRAM_AUTH_URL
    query = {
        'app_id': setting.INSTAGRAM_APP_ID,
        'redirect_uri': setting.INSTAGRAM_REDIRECT_URL,
        'scope': 'user_profile,user_media',
        'response_type': 'code'
    }
    return url + '?' + urlencode(query)


def get_access_token(auth_code):
    url = setting.INSTAGRAM_ACCESS_TOKEN_URL
    data = {
        'app_id': setting.INSTAGRAM_APP_ID,
        'app_secret': setting.INSTAGRAM_SECRET,
        'grant_type': 'authorization_code',
        'redirect_uri': setting.INSTAGRAM_REDIRECT_URL,
        'code': auth_code
    }
    res = requests.post(url, data=data)
    if res.status_code == 200:
        data = json.loads(res.text)
        return data['access_token']


def convert_media(data):
    return {
        'media_id': data['id'],
        'caption': data['caption'] if 'caption' in data else '',
        'type': data['media_type'],
        'permalink': data['permalink'],
        'thumbnail': data['thumbnail_url'] if 'thumbnail_url' in data else data['media_url'],
        'created': datetime.strptime(data['timestamp'], '%Y-%m-%dT%H:%M:%S%z')
    }
