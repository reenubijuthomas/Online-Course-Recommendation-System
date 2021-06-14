from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.views import register, login, logout


class TestUrls(SimpleTestCase):

    def test_register_url_resolves(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func, register)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, login)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, logout)
