from django.test import SimpleTestCase
from django.urls import reverse, resolve
from course.views import courses, coursepage, rate


class TestUrls(SimpleTestCase):

    def test_courses_url_resolves(self):
        url = reverse('courses')
        self.assertEqual(resolve(url).func, courses)

    def test_coursepage_url_resolves(self):
        url = reverse('coursepage', args=[1])
        self.assertEqual(resolve(url).func, coursepage)

    def test_rate_url_resolves(self):
        url = reverse('rate', args=[1])
        self.assertEqual(resolve(url).func, rate)

