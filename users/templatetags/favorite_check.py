from django import template
from users.models import UserFavorite, CustomUser
from blogpost.models.city_page import CityPage
from django.contrib.contenttypes.models import ContentType

register = template.Library()


@register.simple_tag(name='is_city_in_fav')
def city_in_favorite(id,current_u_id):
    flag = False
    content_type_obj = ContentType.objects.get_for_model(CityPage)
    if UserFavorite.objects.filter(object_id=id, content_type=content_type_obj, user=current_u_id).exists():
        flag = True
    return flag


@register.simple_tag(name='is_user_in_fav')
def user_in_favorite(id,current_u_id):
    flag = False
    content_type_obj = ContentType.objects.get_for_model(CustomUser)
    if UserFavorite.objects.filter(object_id=id, content_type=content_type_obj, user=current_u_id).exists():
        flag = True
    return flag