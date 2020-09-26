from django import template


register = template.Library()


@register.simple_tag(name='see_more')
def check_see_more(caption):
    result = dict()
    result['caption1'] = caption[:221]
    result['caption2'] = caption[221:]
    return result
