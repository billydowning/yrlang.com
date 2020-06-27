from blogpost.models.city_page import CityPage
from blogpost.models.modelpost import BlogPostPage
from blogpost.models.brucke_page import BruckePage

def city_list_view(request):
    city_list = CityPage.objects.all()
    return {"city_list": city_list}

def post_list_view(request):
    blog_list = BruckePage.objects.all().order_by("?")[:3]
    for i in blog_list:
        print(i.image)
    return {"blog_list":blog_list}

