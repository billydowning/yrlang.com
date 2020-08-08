from blogpost.models.city_page import CityPage
from blogpost.models.modelpost import BlogPostPage
from blogpost.models.brucke_page import BruckePage


def city_list_view(request):
    city_list = CityPage.objects.all().order_by("?")[:3]
    if city_list:
        parent_of_city = city_list.first().get_parent()
        return {"city_parent": parent_of_city  ,"city_list": city_list}
    return {}


def post_list_view(request):
    blog_list = BruckePage.objects.all().order_by("?")[:3]
    return {"blog_list": blog_list}

