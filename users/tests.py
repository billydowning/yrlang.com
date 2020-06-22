from django.test import TestCase

from .forms import ClientSignupForm, ProfessionalSignupForm

# Create your tests here.


class ClientSignUpTesting(TestCase):

    def test_signup_page(self):
        response = self.client.get('http://127.0.0.1:8000/users/client_signup')

        self.assertEquals(response.status_code, 200, "Done0")
        # self.assertNotContains(response, 'search')
        self.assertContains(response, 'submit')
        self.assertContains(response, 'Sign Up')
        self.assertContains(response, 'id_password2')
        self.assertContains(response, 'Professional Signup')
        self.assertTemplateUsed(response, 'account/signup.html')

    def test_signup_form_valid(self):
        data = {
            'email': 'shivam@gmail.com',
            'username': 'shivam',
            'password1': 'joshi123',
            'password2': 'joshi123',
        }
        form = ClientSignupForm(data=data)
        self.assertTrue(form.is_valid())

    def test_signup_form_invalid(self):
        data = {
            'email': 'shivam@gmail.com',
            'username': 'shivam',
            'password1': 'joshi123',
            'password2': 'joshi124',
        }
        form = ClientSignupForm(data=data)
        self.assertFalse(form.is_valid())


class ProfessionalSignUpTesting(TestCase):

    def test_signup_page(self):
        response = self.client.get('http://127.0.0.1:8000/users/professional_signup')

        self.assertEquals(response.status_code, 200, "Done0")
        self.assertContains(response, 'submit')
        self.assertContains(response, 'Sign Up')
        self.assertContains(response, 'id_password2')
        self.assertTemplateUsed(response, 'account/professional_signup.html')

    def test_signup_form_valid(self):
        data = {
            'email': 'JenniferSDennis@rhyta.com',
            'username': 'Jennifer',
            'password1': 'joshi123',
            'password2': 'joshi123',
        }
        form = ProfessionalSignupForm(data=data)
        self.assertTrue(form.is_valid())

    def test_signup_form_invalid(self):
        data = {
            'email': 'JenniferSDennis@rhyta.com',
            'username': 'Jennifer',
            'password1': 'joshi123',
            'password2': 'joshi124',
        }
        form = ProfessionalSignupForm(data=data)
        self.assertFalse(form.is_valid())


class LoginTesting(TestCase):

    def test_login_page(self):
        response = self.client.get('http://127.0.0.1:8000/accounts/login/')

        self.assertEquals(response.status_code, 200, "Done0")
        self.assertContains(response, 'submit')
        self.assertContains(response, 'sign up')
        self.assertContains(response, 'id_login')
        self.assertContains(response, 'id_password')
        self.assertContains(response, 'Forgot Password?')
        self.assertContains(response, 'id_remember')
        self.assertTemplateUsed(response, 'account/login.html')
