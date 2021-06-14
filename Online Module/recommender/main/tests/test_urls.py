from django.test import SimpleTestCase
from django.urls import reverse, resolve
from main.views import profile, main


#class TestUrls(SimpleTestCase):
#
#    def test_main_url_resolves(self):
#        url = reverse('home')
#        print(resolve(url))
#        self.assertEqual(resolve(url).func, main)
#
#    def test_profile_url_resolves(self):
#        url = reverse('profile')
#        self.assertEqual(resolve(url).func, profile)
