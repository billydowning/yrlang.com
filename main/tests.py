from django.test import TestCase
from django.urls import reverse

from users.models import CustomUser, UserRole

# Create your tests here.


def create_user_role_client():
    return UserRole.objects.create(name=UserRole.CLIENT)


def create_user_role_provider():
    return UserRole.objects.create(name=UserRole.PROVIDER)


def create_client():
    obj = CustomUser.objects.create(
        email='shivam@gmail.com',
        username='shivam',
        is_client=True,
    )
    obj.user_role.add(create_user_role_client())
    obj.save()
    return obj


def create_provider():
    obj = CustomUser.objects.create(
        email='JenniferSDennis@rhyta.com',
        username='Jennifer',
        is_client=False,
        is_private=False
    )
    obj.user_role.add(create_user_role_provider())
    obj.save()
    return obj


class HomePageTest(TestCase):

    def test_home_page(self):
        response = self.client.get('http://127.0.0.1:8000/')

        self.assertEquals(response.status_code, 200, "Done0")
        self.assertEquals(response.context['banner'], "You Are not logged in ")
        self.assertContains(response=response, text='search')
        self.assertTemplateUsed(response, 'home.html')
