from django import template

from users.models import UserRole

register = template.Library()


@register.simple_tag(name='is_client')
def ckeck_is_client(*args, **kwargs):
    return UserRole.CLIENT == kwargs.get('user_role')


@register.simple_tag(name='client')
def check_is_client(user):
    return user.user_role.all().filter(name=UserRole.CLIENT).exists()


@register.simple_tag(name='provider')
def check_is_provider(user):
    return user.user_role.all().filter(name=UserRole.PROVIDER).exists()

@register.simple_tag(name='localite')
def check_is_localite(user):
    return user.user_role.all().filter(name=UserRole.LOCALITE).exists()


@register.simple_tag(name='is_provider')
def ckeck_is_provider(*args, **kwargs):
    return UserRole.PROVIDER == kwargs.get('user_role')


@register.simple_tag(name='is_localite')
def ckeck_is_localite(*args, **kwargs):
    return UserRole.LOCALITE == kwargs.get('user_role')


@register.simple_tag(name='language_verifer')
def check_is_languag_verifer(user):
    return user.user_role.all().filter(name=UserRole.LANGUAGE_VERIFIER).exists()

@register.simple_tag(name='is_language_veri')
def check_is_languag_verifer_session(*args, **kwargs):
    return UserRole.LANGUAGE_VERIFIER == kwargs.get('user_role')