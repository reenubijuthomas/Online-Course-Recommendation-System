from django.test import SimpleTestCase
from django.urls import reverse, resolve
from recommendations.views import recommendation


class TestUrls(SimpleTestCase):

    def test_recommendation_url_resolves(self):
        url = reverse('recommendation')
        self.assertEqual(resolve(url).func, recommendation)

