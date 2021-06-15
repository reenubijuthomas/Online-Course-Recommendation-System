from django.test import TestCase, Client
from django.urls import reverse
from course.models import Course, Rating, Chapter
from django.contrib.auth.models import User, auth


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        self.courses_url = reverse('courses')
        self.coursepage_url = reverse('coursepage',args=[1])
        self.rate_url = reverse('rate', args=[1])
        self.chapter_url = reverse('chapter',args=[1, 1])

        self.user = User.objects.create_user(username="testuser", email="testuser@email.com")
        self.user.set_password('123456')
        self.user.save()
        self.client.login(username='testuser', password="123456")

        course = Course()
        course.pk = 1
        course.name = "testCourse"
        course.topics = "testTopics"
        course.save()
        chapter = Chapter()
        chapter.pk = 1
        chapter.name = "Chapter 1"
        chapter.course = course
        chapter.video = "www.youtube.com"
        chapter.save()

    def test_courses_GET(self):
        response = self.client.get(self.courses_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "courses.html")

    def test_coursepage_logged_in_GET(self):
        self.coursepage_url = reverse('coursepage',args=[1])
        response = self.client.get(self.coursepage_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "coursepage.html")

    def test_coursepage_anonymous_GET(self):
        self.client.logout()
        response = self.client.get(self.coursepage_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "coursepage.html")

    def test_rate_GET(self):
        response = self.client.get(self.rate_url)

        self.assertEqual(response.status_code, 302)

    def test_rate_invalid_rating_POST(self):
        response = self.client.post(self.rate_url, {
            "rating": "0"
        })

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Rating.objects.filter(user=self.user).exists())

    def test_rate_valid_rating_POST(self):
        response = self.client.post(self.rate_url, {
            "rating": "1"
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Rating.objects.filter(user=self.user).exists())

    def test_chapter_GET(self):
        response = self.client.get(self.chapter_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("chapter.html")




