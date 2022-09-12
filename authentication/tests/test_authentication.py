from django.contrib.auth import get_user_model, authenticate
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class SignInTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test_010',
                                                         password='Test12345#test',
                                                         email='test010@example.com')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        user = authenticate(username='test_010', password='Test12345#test')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username='wrong', password='Test12345#test')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_password(self):
        user = authenticate(username='test_010', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)


class SignInViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test010',
                                                         password='Test12345#test',
                                                         email='test010@example.com')

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        response = self.client.post('/authentication/login/', {'username': 'test010', 'password': 'Test12345#test'})
        self.assertTrue(response.data['authenticated'])

    def test_wrong_username(self):
        response = self.client.post('/authentication/login/', {'username': 'wrong', 'password': 'Test12345#test'})
        self.assertFalse(response.data['authenticated'])

    def test_wrong_password(self):
        response = self.client.post('/authentication/login/', {'username': 'test010', 'password': 'wrong'})
        self.assertFalse(response.data['authenticated'])


class BaseTest(TestCase):
    def setUp(self):
        self.register_url = reverse('authentication:register')
        self.login_url = reverse('authentication:login_user')
        self.user = {
            'email': 'testuser1@gamil.com',
            'username': 'username',
            'password1': 'password',
            'password2': 'password',
            'first_name': 'first_name',
            'last_name': 'last_name'
        }
        return super().setUp()


class RegisterTest(BaseTest):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/register.html')
        self.assertTemplateNotUsed(response, 'authentication/login.html')

    def test_can_register_user(self):
        response = self.client.post(self.register_url, self.user, format='text/html')
        self.assertEqual(response.status_code, 302)


class LoginTest(BaseTest):
    def test_can_access_page(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/login.html')
        self.assertTemplateNotUsed(response, 'authentication/register.html')

    def test_login_success(self):
        self.client.get(self.register_url, self.user, format='text/html')
        user = User.objects.filter(email=self.user['email']).first()
        user.is_active = True
        user.save()
        response = self.client.post(self.login_url, self.user, format='text/html')
        self.assertEqual(response.status_code, 302)
