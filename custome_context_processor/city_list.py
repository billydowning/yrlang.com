from blogpost.models.city_page import CityPage

def city_list_view(request):
    city_list = CityPage.objects.all()
    return {"city_list": city_list}
