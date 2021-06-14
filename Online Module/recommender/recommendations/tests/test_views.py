from django.test import TestCase, Client
from django.urls import reverse
from course.models import Course, Rating
from main.models import UserProfiles
from django.contrib.auth.models import User, auth


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.recommendation_url = reverse('recommendation')
        self.user = User.objects.create_user(username="testuser", email="testuser@email.com")
        self.user.set_password('123456')
        self.user.save()
        self.client.login(username='testuser', password="123456")

        course = Course()
        course.pk = 1
        course.name = "testCourse"
        course.topics = "testTopics"
        course.save()

    def test_recommendation_with_userprofile_GET(self):
        userprofile = UserProfiles()
        userprofile.user = self.user
        userprofile.topics = "testTopics"
        userprofile.pk = 1
        userprofile.save()
        response = self.client.get(self.recommendation_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recommendation.html")

    def test_recommendation_without_userprofile_GET(self):
        response = self.client.get(self.recommendation_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "msg.html")











